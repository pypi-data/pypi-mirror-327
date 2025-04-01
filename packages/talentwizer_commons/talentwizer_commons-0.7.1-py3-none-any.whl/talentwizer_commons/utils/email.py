import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.message import EmailMessage
from urllib.parse import unquote
from pydantic import BaseModel, EmailStr
from google.oauth2.credentials import Credentials
from google.auth.exceptions import RefreshError
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from msal import ConfidentialClientApplication
import requests
from talentwizer_commons.app.engine import get_chat_engine
from llama_index.core.chat_engine.types import BaseChatEngine
from google.auth.transport.requests import Request
from fastapi import APIRouter, HTTPException, Request, Depends
from dotenv import load_dotenv
from typing import List, Optional
import base64
import os
load_dotenv()
import logging
from datetime import datetime, timedelta
import pytz
from kombu.exceptions import OperationalError
from redis import Redis
import redis
from celery.exceptions import TaskError
from celery.result import AsyncResult
from talentwizer_commons.utils.db import mongo_database
import logging
from .celery_init import celery_app, send_scheduled_email, get_test_delay  # Add get_test_delay here
import asyncio

# Create a Redis connection pool (add after imports)
REDIS_POOL = redis.ConnectionPool.from_url(
    os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0'),
    decode_responses=True,
    socket_timeout=5,
    retry_on_timeout=True,
    health_check_interval=30
)

def get_redis_client() -> redis.Redis:
    """Get a Redis client from the connection pool."""
    return redis.Redis(connection_pool=REDIS_POOL)

email_router = e = APIRouter()
logger = logging.getLogger(__name__)

sequence_collection = mongo_database["email_sequences"]
sequence_audit_collection = mongo_database["email_sequence_audits"]

class TokenData(BaseModel):
    accessToken: str
    refreshToken: str
    clientId: str
    clientSecret: str
    idToken: str
    userEmail: str
    scope: str

class EmailPayload(BaseModel):
    from_email: Optional[EmailStr] = None
    to_email: Optional[List[EmailStr]] = None
    cc: Optional[List[EmailStr]] = None
    subject: Optional[str] = None
    body: Optional[str] = None
    attachments: Optional[List[str]] = None

@e.post("/send/admin")    
async def send_email_by_admin_account(emailPayload: EmailPayload):
    from_email = os.getenv("ADMIN_EMAIL")
    userEmail: str
    scope: str

class EmailPayload(BaseModel):
    from_email: Optional[EmailStr] = None
    to_email: Optional[List[EmailStr]] = None
    cc: Optional[List[EmailStr]] = None
    subject: Optional[str] = None
    body: Optional[str] = None
    attachments: Optional[List[str]] = None

@e.post("/send/admin")    
async def send_email_by_admin_account(emailPayload: EmailPayload):
    from_email = os.getenv("ADMIN_EMAIL")
    if not from_email:
        logging.error("Admin email is not set in environment variables")
        return False

    to_email = emailPayload.to_email
    subject = emailPayload.subject
    body = emailPayload.body
    attachments = emailPayload.attachments

    comma_separated_emails = ",".join(to_email) if to_email else ""
    if not comma_separated_emails:
        logging.error("Recipient email addresses are empty or malformed")
        return False

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = unquote(comma_separated_emails)

    if subject:
        msg['Subject'] = subject
    else:
        logging.warning("Email subject is empty")

    if body:
        msg.attach(MIMEText(body, 'plain'))
    else:
        logging.warning("Email body is empty")

    # Attach files if any
    if attachments:
        for attachment_path in attachments:
            try:
                with open(attachment_path, "rb") as attachment:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment.read())
                    encoders.encode_base64(part)
                    filename = os.path.basename(attachment_path)
                    part.add_header('Content-Disposition', f'attachment; filename={filename}')
                    msg.attach(part)
            except FileNotFoundError:
                logging.error(f"Attachment file not found: {attachment_path}")
            except PermissionError:
                logging.error(f"Permission denied for attachment file: {attachment_path}")
            except Exception as e:
                logging.error(f"Unexpected error attaching file {attachment_path}: {e}")
    
    try:
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(from_email, os.getenv("ADMIN_EMAIL_PASSWORD"))
        s.sendmail(from_email, unquote(comma_separated_emails), msg.as_string())
        s.quit()
        logging.info("Email sent successfully through admin email")
        return True
    except smtplib.SMTPAuthenticationError:
        logging.error("SMTP authentication failed. Check ADMIN_EMAIL and ADMIN_EMAIL_PASSWORD")
    except smtplib.SMTPConnectError as e:
        logging.error(f"SMTP connection error: {e}")
    except smtplib.SMTPRecipientsRefused:
        logging.error(f"All recipients were refused: {comma_separated_emails}")
    except smtplib.SMTPException as e:
        logging.error(f"SMTP error occurred: {e}")
    except Exception as e:
        logging.error(f"Unexpected error while sending email: {e}")
    return False
        
def create_message(emailPayload):
    sender = emailPayload.from_email
    to = emailPayload.to_email
    subject = emailPayload.subject
    message_text = emailPayload.body

    # Ensure the message_text is properly formatted as HTML
    message_text = f"""
    <html>
    <head></head>
    <body>
        {message_text}
    </body>
    </html>
    """

    # Convert the list of to_email addresses to a comma-separated string
    to_emails = ', '.join(to) if to else ''

    # Create the email message
    message = MIMEMultipart('alternative')
    message['to'] = to_emails
    message['from'] = sender
    message['subject'] = subject

    print("original msg :: " + message_text)

    # Attach the message text as HTML
    html_part = MIMEText(message_text, 'html', 'utf-8')
    message.attach(html_part)

    print("html msg :: " + str(message))

    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
    return {'raw': raw_message}


def send_message(service, user_id, message):
    try:
        message = service.users().messages().send(userId=user_id, body=message).execute()
        logging.info('Message Id: %s' % message['id'])
        logging.info('Message Id: %s' % message['id'])
        return message
    except HttpError as error:
        logging.error('An error occurred: %s' % error)
        return None

@e.post("/send")
async def send_email_from_user_email(tokenData: dict, emailPayload: EmailPayload):
    def send_message_gmail(service, user_id, message):
        # Send email via Gmail API
        service.users().messages().send(userId=user_id, body=message).execute()

    def send_message_microsoft(access_token, payload):
        # Ensure payload is converted to a dictionary or JSON
        url = "https://graph.microsoft.com/v1.0/me/sendMail"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        # Convert EmailPayload to a dictionary if it's not already
        if isinstance(payload, EmailPayload):
            payload_dict = {
                "message": {
                    "subject": payload.subject,
                    "body": {
                        "contentType": "HTML",  # Ensure content type is HTML
                        "content": payload.body
                    },
                    "toRecipients": [{"emailAddress": {"address": email}} for email in payload.to_email]
                }
            }
            if payload.cc:
                payload_dict["message"]["ccRecipients"] = [
                    {"emailAddress": {"address": email}} for email in payload.cc
                ]
            if payload.attachments:
                payload_dict["message"]["attachments"] = payload.attachments
        else:
            payload_dict = payload  # Assume it's already in a serializable format

        response = requests.post(url, headers=headers, json=payload_dict)
        if response.status_code not in (200, 202):
            raise RuntimeError(f"Error sending email via Microsoft Graph API: {response.text}")

    try:
        # Determine the provider based on scopes
        if "https://www.googleapis.com/auth/gmail.send" in tokenData.get("scope", ""):
            # Handle Gmail account
            SCOPES = tokenData["scope"].split()
            creds = Credentials(
                token=tokenData["accessToken"],
                refresh_token=tokenData["refreshToken"],
                token_uri="https://oauth2.googleapis.com/token",
                client_id=tokenData["clientId"],
                client_secret=tokenData["clientSecret"],
                scopes=SCOPES
            )
            try:
                gmail_service = build('gmail', 'v1', credentials=creds)
                message = create_message(emailPayload)
                send_message_gmail(gmail_service, 'me', message)
                return {"status_code": 200, "message": "Email sent successfully."}
            except RefreshError:
                # Refresh token logic for Gmail
                creds.refresh(Request())
                tokenData["accessToken"] = creds.token
                tokenData["refreshToken"] = creds.refresh_token
                gmail_service = build('gmail', 'v1', credentials=creds)
                message = create_message(emailPayload)
                send_message_gmail(gmail_service, 'me', message)
                return {"status_code": 200, "message": "Email sent successfully after token refresh."}

        elif "Mail.Send" in tokenData.get("scope", ""):
            # Handle Microsoft account
            access_token = tokenData["accessToken"]
            refresh_token = tokenData["refreshToken"]
            client_id = tokenData["clientId"]
            client_secret = tokenData["clientSecret"]
            authority = tokenData.get("authority", "https://login.microsoftonline.com/common")

            try:
                send_message_microsoft(access_token, emailPayload)
                return {"status_code": 200, "message": "Email sent successfully."}
            except RuntimeError:
                # Refresh token logic for Microsoft
                app = ConfidentialClientApplication(
                    client_id, authority=authority, client_credential=client_secret
                )
                result = app.acquire_token_by_refresh_token(refresh_token, scopes=["Mail.Send"])
                if "access_token" in result:
                    tokenData["accessToken"] = result["access_token"]
                    send_message_microsoft(result["access_token"], emailPayload)
                    return {"status_code": 200, "message": "Email sent successfully after token refresh."}
                else:
                    raise RuntimeError("Failed to refresh Microsoft token.")

        else:
            raise ValueError("Unsupported email provider or missing scope in tokenData.")

    except Exception as e:
        logging.error("Unexpected error while sending email", exc_info=True)
        raise RuntimeError(f"Unexpected error: {str(e)}") from e


@e.get("/generate")
async def generate_personalised_email(
    company_name:str,
    person_name: str,
    person_summary: str,
    title: str,
    chat_engine: BaseChatEngine = Depends(get_chat_engine),
):
    prompt = "You are an expert recruiter and co-pilot for recruitment industry. "
    prompt += "Help generate a Email based on Job Title, Person Summary and Person Name to be sent to the potential candidate. " 
    prompt+= "Company Name: " + company_name +"\n"
    
    if(person_name!=""):
      prompt += "Person Name: " + str(person_name) + "\n"
      
    prompt += "Person Summary:" + str(person_summary) + "\n"
    prompt += "Job Title:" + str(title) + "\n"
    
    prompt += "Try to Write like this: Hi Based on your description your profile is being shortlisted/rejeected etc. Try to Write in about 150 words. Do not Add Any Types Of Salutations. At Ending Just Write Recruiting Team and There Company Name"
    response=chat_engine.chat(prompt)
    return response.response


@e.get("/generate/summary")
async def generate_summary(
    job_title: str,
    person_summary: str
):
    chat_engine: Optional[BaseChatEngine] = None
    try:
        # Validate inputs
        if not job_title.strip():
            raise ValueError("Job title cannot be empty.")
        if not person_summary.strip():
            raise ValueError("Person summary cannot be empty.")

        # Prepare the prompt
        prompt = (
            "You are an expert recruiter and co-pilot for the recruitment industry. "
            f"Job Title: {job_title}\n"
            f"Person Summary: {person_summary}\n"
            "Summarise person's experience and expertise based on the given Person Summary "
            "in the context of an interview mail. Personalise the content as if you are "
            "writing an email or talking to the candidate directly to show him/her as the best fit for the job. \n"
            "The email should be concise and engaging.\n"
            "Example:  based on your experience and expertise, you are a perfect fit for the job. "
            "Do not write full email content but just a summary of the candidate's experience with "
            "regard to the given job title. Try to summarise in about 50 to 60 words."
        )

        # Resolve chat_engine if not provided
        if chat_engine is None:
            chat_engine = get_chat_engine()

        # Call the chat engine
        response = chat_engine.chat(prompt)
        
        # Ensure the response is valid
        if not response or not hasattr(response, "response"):
            raise ValueError("Chat engine did not return a valid response.")

        return response.response

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while generating the summary.")


# Utility function to replace placeholders in the email template
async def populate_template_v1(template: str, person: dict, job_title: str) -> str:
    """
    Populates a template with data from the provided person and job title. 

    Args:
        template: The template string with placeholders.
        person: A dictionary containing information about the person.
        job_title: The target job title.

    Returns:
        The populated template string.

    Raises:
        ValueError: If the input parameters are invalid.
        HTTPException: If an error occurs during template population.
    """

    try:
        # Validate inputs
        if not isinstance(template, str) or not template.strip():
            raise ValueError("Template must be a non-empty string.")
        if not isinstance(person, dict):
            raise ValueError("Person must be a dictionary.")
        if not isinstance(job_title, str) or not job_title.strip():
            raise ValueError("Job title must be a non-empty string.")

        # Generate the brief summary
        brief_summary: Optional[str] = await generate_summary(job_title, person.get("summary", ""))

        if not brief_summary:
            raise ValueError("Failed to generate a brief summary for the candidate.")

        # Replace placeholders conditionally
        populated_template = template

        if "{{First Name}}" in template:
            populated_template = populated_template.replace("{{First Name}}", person.get("name", "Candidate"))

        if "{{Current Company}}" in template:
            populated_template = populated_template.replace("{{Current Company}}", person.get("work_experience", [{}])[0].get("company_name", "Company")) 

        if "{{Current Job Title}}" in template:
            # populated_template = populated_template.replace("{{Current Job Title}}", person.get("occupation", "Job Title"))
             populated_template = populated_template.replace("{{Current Job Title}}", person.get("work_experience", [{}])[0].get("designation", "Job Title")) 
        if "{*Brief mention of the candidate’s relevant skills.*}" in template:
            populated_template = populated_template.replace("{*Brief mention of the candidate’s relevant skills.*}", brief_summary)

        return populated_template

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while populating the template.")

async def populate_template_v2(template: str, person: dict, job_title: str) -> str:
    try:
        # Validate inputs
        if not isinstance(template, str) or not template.strip():
            raise ValueError("Template must be a non-empty string.")
        if not isinstance(person, dict):
            raise ValueError("Person must be a dictionary.")
        if not isinstance(job_title, str) or not job_title.strip():
            raise ValueError("Job title must be a non-empty string.")

        # Fetch values with defaults
        full_name = person.get("full_name", "Candidate")
        current_company = person.get("experience", [{}])[0].get("company_name", "Company")
        person_job_title = person.get("experience", [{}])[0].get("title", "Title")
        summary = person.get("summary", "skills and experience")

        # Generate the brief summary
        brief_summary: Optional[str] = await generate_summary(job_title, summary)

        if not brief_summary:
            raise ValueError("Failed to generate a brief summary for the candidate.")

        # Replace placeholders in the template
        populated_template = (
            template.replace("{{Full Name}}", full_name)
            .replace("{{Current Company}}", current_company)
            .replace("{{Current Job Title}}", person_job_title)
            .replace("{{Client Company}}", "our company")
            .replace("{*Brief mention of the candidate’s relevant skills.*}", brief_summary)
            .replace("{{Client Job Title}}", job_title)
        )

        return populated_template

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while populating the template.")
    
async def send_failure_report(reports: List[dict]):
    try:
        for report in reports:
            report_payload = EmailPayload(
                to_email=[report["to_email"]],
                subject=report["subject"],
                body=report["body"]
            )
            await send_email_by_admin_account(report_payload)
    except Exception as e:
        logging.error("Failed to send failure report emails", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to send failure report emails: {str(e)}")


send_email_task = send_scheduled_email

async def check_redis_queue(redis_instance: redis.Redis, key: str, task_id: str) -> bool:
    """Safely check Redis queue existence and type."""
    try:
        # Check if key exists and is the right type
        key_type = redis_instance.type(key)
        if key_type == b'zset':
            return redis_instance.zscore(key, task_id) is not None
        elif key_type == b'none':
            # Initialize as sorted set if doesn't exist
            redis_instance.zadd(key, {task_id: float(datetime.now().timestamp())})
            return True
        else:
            # Wrong type, reinitialize
            redis_instance.delete(key)
            redis_instance.zadd(key, {task_id: float(datetime.now().timestamp())})
            return True
    except Exception as e:
        logger.error(f"Redis operation failed for key {key}: {str(e)}")
        return False

async def schedule_email(email_payload: dict, scheduled_time: datetime = None, timezone: str = None, token_data: dict = None) -> str:
    """Schedule an email to be sent at a specific time."""
    redis_instance = None
    try:
        # Get Redis client from pool
        redis_instance = get_redis_client()
        
        # Test connection
        if not redis_instance.ping():
            raise ConnectionError("Could not connect to Redis")

        # Fix email payload issue - move content to body
        if 'content' in email_payload and 'body' not in email_payload:
            email_payload['body'] = email_payload.pop('content')
            
        # Check test mode first before anything else
        test_delay = get_test_delay()
        if test_delay:
            logger.info(f"Test mode enabled, using {test_delay} seconds delay")
            scheduled_time = datetime.utcnow() + timedelta(seconds=test_delay)
            logger.info(f"Overriding scheduled time to: {scheduled_time}")

        logger.info(f"Final scheduling time: {scheduled_time}")
        logger.info(f"Email payload: {email_payload}")
        
        # Schedule task with token data
        task = send_email_task.apply_async(
            kwargs={
                'email_payload': email_payload,
                'scheduled_time': scheduled_time.isoformat() if scheduled_time else None,
                'token_data': token_data
            },
            eta=scheduled_time,
            queue='email_queue',
            routing_key='email.send'
        )
        
        logger.info(f"Task scheduled with ID: {task.id}")
        
        # Create audit record
        try:
            audit_data = {
                "schedule_id": task.id,
                "email_payload": email_payload,
                "scheduled_time": scheduled_time,
                "status": "SCHEDULED",
                "token_data": token_data,
                "created_at": datetime.utcnow()
            }
            
            if not sequence_audit_collection.find_one({"schedule_id": task.id}):
                sequence_audit_collection.insert_one(audit_data)
                logger.info(f"Audit record created for task {task.id}")
        except Exception as e:
            logger.error(f"Error managing audit record: {str(e)}")

        # Wait for task to appear in Redis
        max_attempts = 5
        for attempt in range(max_attempts):
            if await check_redis_queue(redis_instance, 'unacked', task.id) or \
               await check_redis_queue(redis_instance, 'reserved', task.id):
                logger.info(f"Task {task.id} verified in Redis")
                return str(task.id)
            
            logger.warning(f"Task not found in Redis, attempt {attempt + 1}/{max_attempts}")
            await asyncio.sleep(0.5)
            
        raise Exception("Task was not properly scheduled in Redis")

    except Exception as e:
        logger.error(f"Failed to schedule email: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Clean up Redis connection if needed
        if redis_instance:
            try:
                redis_instance.close()
            except:
                pass

@e.get("/scheduled-email/{task_id}")
async def check_scheduled_email(task_id: str):
    """Check the status of a scheduled email task."""
    try:
        result = AsyncResult(task_id, app=celery_app)
        return {
            "task_id": task_id,
            "status": result.status,
            "result": result.result if result.ready() else None
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to check task status: {str(e)}")

@e.get("/scheduled-emails")
async def list_scheduled_emails():
    """List all scheduled email tasks in Redis."""
    try:
        redis_client = redis.Redis.from_url(os.getenv('CELERY_BROKER_URL'))
        scheduled_tasks = redis_client.zrange('unacked', 0, -1)
        return {
            "scheduled_tasks": [task.decode() for task in scheduled_tasks]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list scheduled tasks: {str(e)}")

# @e.post("/schedule-email")
# async def schedule_email(email_payload: EmailPayload, delay: int, timezone: str, time: str, days: int, day_type: str):
#     # Calculate the delay based on the provided details
#     user_timezone = pytz.timezone(timezone)
#     now = datetime.now(user_timezone)
#     scheduled_time = datetime.strptime(time, "%H:%M").time()
#     scheduled_datetime = datetime.combine(now, scheduled_time)

#     if day_type == "business_days":
#         business_days_to_add = days
#         current_day = now.weekday()
#         days_to_add = (business_days_to_add - (4 - current_day)) % 5
#         if days_to_add <= 0:
#             days_to_add += 5
#         scheduled_datetime += timedelta(days=days_to_add)
#     else:
#         scheduled_datetime += timedelta(days=days)

#     delay_seconds = (scheduled_datetime - now).total_seconds()
#     if delay_seconds < 0:
#         delay_seconds = 0

#     send_email_task.apply_async(args=[email_payload.dict(), int(delay_seconds)], countdown=int(delay_seconds))
#     return {"message": "Email scheduled successfully"}

async def refresh_token(token_data: dict) -> dict:
    """Refresh the access token using the refresh token."""
    try:
        if "https://www.googleapis.com/auth/gmail.send" in token_data.get("scope", ""):
            # Refresh Gmail token
            creds = Credentials(
                token=token_data["accessToken"],
                refresh_token=token_data["refreshToken"],
                token_uri="https://oauth2.googleapis.com/token",
                client_id=token_data["clientId"],
                client_secret=token_data["clientSecret"],
                scopes=token_data["scope"].split()
            )
            creds.refresh(Request())
            return {
                **token_data,
                "accessToken": creds.token,
                "refreshToken": creds.refresh_token
            }
        elif "Mail.Send" in token_data.get("scope", ""):
            # Refresh Microsoft token
            app = ConfidentialClientApplication(
                token_data["clientId"],
                authority=token_data.get("authority", "https://login.microsoftonline.com/common"),
                client_credential=token_data["clientSecret"]
            )
            result = app.acquire_token_by_refresh_token(
                token_data["refreshToken"],
                scopes=["Mail.Send"]
            )
            if "access_token" not in result:
                raise Exception("Failed to refresh token")
            return {
                **token_data,
                "accessToken": result["access_token"]
            }
    except Exception as e:
        logging.error(f"Error refreshing token: {str(e)}")
        raise

@celery_app.task
def send_email_with_retry(email_payload: dict, token_data: dict, max_retries: int = 3):
    """Send email with token refresh retry logic."""
    for attempt in range(max_retries):
        try:
            if attempt > 0:
                # Refresh token before retrying
                token_data = refresh_token(token_data)
            
            result = send_email_from_user_email(token_data, EmailPayload(**email_payload))
            if result["status_code"] == 200:
                return result
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            logging.warning(f"Email send attempt {attempt + 1} failed, retrying...")
            continue

@e.get("/scheduled-tasks/stats")
async def get_scheduled_tasks_stats():
    """Get statistics about scheduled tasks."""
    stats = {
        "redis": {"status": "unknown"},
        "celery": {"status": "unknown"},
        "database": {"status": "unknown"}
    }

    try:
        # Redis checks with connection pooling and error handling
        try:
            redis_pool = redis.ConnectionPool.from_url(
                os.getenv('CELERY_BROKER_URL'),
                socket_timeout=5,
                socket_connect_timeout=5,
                retry_on_timeout=True,
                health_check_interval=30,
                max_connections=10
            )
            
            redis_client = redis.Redis(connection_pool=redis_pool)
            redis_client.ping()  # Test connection
            
            stats["redis"] = {
                "status": "connected",
                "unacked": redis_client.zcard('unacked'),
                "scheduled": redis_client.zcard('scheduled'),
                "queue_length": redis_client.llen('celery')
            }
        except redis.ConnectionError as e:
            logger.error(f"Redis connection error: {str(e)}")
            stats["redis"].update({
                "status": "disconnected",
                "error": str(e)
            })
        finally:
            if 'redis_pool' in locals():
                redis_pool.disconnect()

        # Celery checks with timeout
        try:
            # Only use supported timeout parameter
            inspector = celery_app.control.inspect(timeout=3.0)
            
            # Check worker availability
            if not inspector.ping():
                raise ConnectionError("No Celery workers responded to ping")
            
            active = inspector.active() or {}
            scheduled = inspector.scheduled() or {}
            reserved = inspector.reserved() or {}
            
            stats["celery"] = {
                "status": "connected",
                "active": sum(len(tasks) for tasks in active.values()),
                "reserved": sum(len(tasks) for tasks in reserved.values()),
                "scheduled": sum(len(tasks) for tasks in scheduled.values())
            }
        except (ConnectionError, TimeoutError, OSError) as e:
            logger.error(f"Celery inspection error: {str(e)}")
            stats["celery"].update({
                "status": "disconnected",
                "error": str(e)
            })

        # Database checks with error handling
        try:
            pipeline = [{"$group": {"_id": "$status", "count": {"$sum": 1}}}]
            audit_counts = list(sequence_audit_collection.aggregate(pipeline))
            
            stats["database"] = {
                "status": "connected",
                "audit_counts": audit_counts
            }
        except Exception as e:
            logger.error(f"Database error: {str(e)}")
            stats["database"].update({
                "status": "error",
                "error": str(e)
            })

        return stats

    except Exception as e:
        logger.error(f"Failed to get task stats: {str(e)}", exc_info=True)
        return {
            "status": "error",
            "error": str(e),
            "component_status": {
                "redis": stats["redis"]["status"],
                "celery": stats["celery"]["status"],
                "database": stats["database"]["status"]
            }
        }

@e.get("/scheduled-tasks/details")
async def list_scheduled_task_details():
    """List all scheduled tasks with their details."""
    try:
        redis_client = redis.Redis.from_url(os.getenv('CELERY_BROKER_URL'))
        scheduled_tasks = []
        
        # Get tasks from Redis
        tasks = redis_client.zrange('unacked', 0, -1, withscores=True)
        
        for task_id, score in tasks:
            try:
                task_id_str = task_id.decode()
                task = AsyncResult(task_id_str, app=celery_app)
                scheduled_time = datetime.fromtimestamp(score)
                
                # Get task info from audit collection
                audit = sequence_audit_collection.find_one({"schedule_id": task_id_str})
                
                if audit:
                    task_info = {
                        "task_id": task_id_str,
                        "status": task.status,
                        "scheduled_time": scheduled_time.isoformat(),
                        "recipient": audit["email_payload"]["to_email"] if audit.get("email_payload") else None,
                        "subject": audit["email_payload"]["subject"] if audit.get("email_payload") else None,
                        "sequence_id": audit.get("sequence_id"),
                        "error": audit.get("error_message"),
                        "sent_time": audit.get("sent_time", "").isoformat() if audit.get("sent_time") else None
                    }
                    scheduled_tasks.append(task_info)
            except Exception as task_error:
                logger.error(f"Error processing task {task_id}: {str(task_error)}", exc_info=True)
                continue
        
        return {
            "scheduled_tasks": scheduled_tasks,
            "total_count": len(scheduled_tasks)
        }
    except Exception as e:
        logger.error(f"Failed to list scheduled tasks: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to list scheduled tasks: {str(e)}")

@e.delete("/scheduled-tasks/{task_id}")
async def cancel_scheduled_task(task_id: str):
    """Cancel a scheduled task."""
    try:
        # Get task from Celery
        task = AsyncResult(task_id, app=celery_app)
        task.revoke(terminate=True)
        
        # Remove from Redis if present
        redis_client = redis.Redis.from_url(os.getenv('CELERY_BROKER_URL'))
        redis_client.zrem('unacked', task_id.encode())
        
        # Update audit record
        result = sequence_audit_collection.update_one(
            {"schedule_id": task_id},
            {
                "$set": {
                    "status": "CANCELLED",
                    "updated_at": datetime.utcnow()
                }
            }
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail=f"Task {task_id} not found in audit collection")
        
        return {
            "message": f"Task {task_id} cancelled successfully",
            "status": "CANCELLED"
        }
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Failed to cancel task: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to cancel task: {str(e)}")

def get_formatted_times(scheduled_time: str | datetime | int | float) -> dict:
    """Convert various time formats to UTC and IST timezones."""
    try:
        # Handle different input types
        if isinstance(scheduled_time, datetime):
            utc_time = scheduled_time.astimezone(pytz.UTC)
        else:
            # Convert to string for consistent handling
            scheduled_time_str = str(scheduled_time)

            try:
                # Try parsing numeric timestamp
                if scheduled_time_str.isdigit() or scheduled_time_str.replace('.', '').isdigit():
                    utc_time = datetime.fromtimestamp(float(scheduled_time_str), tz=pytz.UTC)
                # Try parsing ISO format
                else:
                    # Clean up the time string
                    clean_time = scheduled_time_str.strip()
                    # Remove any trailing Z and replace with proper UTC offset
                    if clean_time.endsWith('Z'):
                        clean_time = clean_time[:-1] + '+00:00'
                    # Add UTC offset if missing
                    elif not any(x in clean_time for x in ['+', '-', 'Z']):
                        clean_time += '+00:00'
                    utc_time = datetime.fromisoformat(clean_time)
                    if utc_time.tzinfo is None:
                        utc_time = pytz.UTC.localize(utc_time)
            except (ValueError, TypeError):
                # If all else fails, try dateutil parser
                from dateutil import parser
                utc_time = parser.parse(scheduled_time_str)
                if utc_time.tzinfo is None:
                    utc_time = pytz.UTC.localize(utc_time)

        # Convert to IST
        ist = pytz.timezone('Asia/Kolkata')
        ist_time = utc_time.astimezone(ist)
        
        return {
            'utc': utc_time.strftime('%Y-%m-%d %I:%M:%S %p UTC'),
            'ist': ist_time.strftime('%Y-%m-%d %I:%M:%S %p IST'),
            'timestamp': int(utc_time.timestamp())
        }
    except Exception as e:
        logger.error(f"Error formatting time {scheduled_time}: {str(e)}", exc_info=True)
        return {
            'utc': str(scheduled_time),
            'ist': 'Invalid date format',
            'timestamp': None
        }

@e.get("/scheduled-tasks/monitor")
async def monitor_scheduled_tasks():
    """Get detailed monitoring information about tasks."""
    try:
        stats = {
            "redis": {"status": "unknown"},
            "celery": {"status": "unknown"},
            "database": {"status": "unknown"},
            "tasks": []
        }

        # Get Redis stats with error handling
        try:
            redis_client = redis.Redis.from_url(
                os.getenv('CELERY_BROKER_URL'),
                decode_responses=True,
                socket_timeout=5
            )
            redis_client.ping()

            stats["redis"] = {
                "status": "connected",
                "tasks": await get_redis_tasks(redis_client)
            }
        except Exception as e:
            logger.error(f"Redis error: {str(e)}")
            stats["redis"]["error"] = str(e)

        # Get scheduled tasks from audit collection
        try:
            scheduled_tasks = list(sequence_audit_collection.find(
                {"status": "SCHEDULED"}
            ))

            for task in scheduled_tasks:
                task_info = await get_task_info(task)
                if task_info:
                    stats["tasks"].append(task_info)
        except Exception as e:
            logger.error(f"Database error: {str(e)}")
            stats["database"]["error"] = str(e)

        return stats

    except Exception as e:
        logger.error(f"Monitor error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

async def get_redis_tasks(redis_client):
    """Get task information from Redis."""
    tasks = []
    try:
        for key in ['unacked', 'scheduled', 'reserved']:
            items = redis_client.zrange(key, 0, -1, withscores=True)
            tasks.extend([{
                "id": item[0],
                "score": item[1],
                "queue": key
            } for item in items])
    except Exception as e:
        logger.error(f"Error getting Redis tasks: {str(e)}")
    return tasks

async def get_task_info(task):
    """Get detailed task information."""
    try:
        task_id = task.get("schedule_id")
        if not task_id:
            return None

        celery_task = AsyncResult(task_id, app=celery_app)
        
        return {
            "task_id": task_id,
            "status": celery_task.status,
            "scheduled_time": task.get("scheduled_time"),
            "email_payload": task.get("email_payload"),
            "token_data_present": bool(task.get("token_data")),
            "token_data": {  # Add redacted token info
                "provider": "gmail" if "gmail.send" in task.get("token_data", {}).get("scope", "") else "microsoft",
                "user_email": task.get("token_data", {}).get("userEmail"),
                "has_refresh_token": bool(task.get("token_data", {}).get("refreshToken"))
            } if task.get("token_data") else None,
            "created_at": task.get("created_at"),
            "celery_info": celery_task.info,
            "test_mode": bool(os.getenv('TEST_MODE') == 'true')
        }
    except Exception as e:
        logger.error(f"Error getting task info: {str(e)}")
        return None

# ... rest of existing code ...