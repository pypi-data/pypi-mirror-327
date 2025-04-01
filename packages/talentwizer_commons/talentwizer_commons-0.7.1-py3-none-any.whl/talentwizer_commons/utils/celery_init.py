import os
from celery import Celery, signals
from celery.states import PENDING, SUCCESS, FAILURE  # Add this import
from kombu import Queue, Exchange
import redis
import logging
from datetime import datetime, timedelta
import json
import asyncio
from bson import ObjectId
from celery.signals import worker_ready, after_setup_logger, after_setup_task_logger, celeryd_after_setup, task_sent, task_received, task_success, task_failure
from celery.schedules import crontab
import threading

logger = logging.getLogger(__name__)

# Add JSON encoder class
class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

# Initialize MongoDB collections
from talentwizer_commons.utils.db import mongo_database
sequence_collection = mongo_database["email_sequences"]
sequence_audit_collection = mongo_database["email_sequence_audits"]

def get_redis_url():
    """Get properly formatted Redis URL"""
    url = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
    if url.startswith('custom_redis://'):
        url = url.replace('custom_redis://', 'redis://')
    return url

# Create the Celery application with proper name and imports
celery_app = Celery(
    'talentwizer_commons',
    broker=get_redis_url(),
    backend=get_redis_url(),
    include=['talentwizer_commons.utils.celery_init']
)

# Update Celery configuration
celery_app.conf.update(
    broker_transport_options={
        'visibility_timeout': 43200,
        'fanout_prefix': True,
        'fanout_patterns': True,
        'global_keyprefix': 'celery:',
        'broker_connection_retry': True,
        'broker_connection_max_retries': None,
        'result_backend_transport_options': {
            'visibility_timeout': 43200,
            'retry_policy': {
                'timeout': 5.0
            }
        },
        'acks_late': True,
        'store_persistent': True
    },
    broker_connection_retry_on_startup=True,
    
    # Task settings
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    task_track_started=True,
    task_ignore_result=False,
    task_store_errors_even_if_ignored=True,
    result_expires=None,
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    task_time_limit=600,
    task_soft_time_limit=300,
    task_send_sent_event=True,
    task_publish_retry=True,
    task_publish_retry_policy={
        'max_retries': 3,
        'interval_start': 0,
        'interval_step': 0.2,
        'interval_max': 0.2,
    },
    
    # Worker settings
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=50,
    worker_max_memory_per_child=50000,
    worker_state_db='/tmp/celery/worker.state',
    worker_state_persistent=True,
    worker_send_task_events=True,
    
    # Queue configuration
    task_queues=(
        Queue('celery', Exchange('celery'), routing_key='celery'),
        Queue('email_queue', Exchange('email_queue'), routing_key='email.#'),
    ),
    task_routes={
        'cleanup_test_duplicates': {
            'queue': 'celery',
            'routing_key': 'celery'
        },
        'send_scheduled_email': {
            'queue': 'email_queue',
            'routing_key': 'email.send'
        }
    },
    task_default_queue='celery',
    task_default_exchange='celery',
    task_default_routing_key='celery',
    
    # Beat schedule configuration
    beat_schedule={
        'cleanup-test-duplicates': {
            'task': 'cleanup_test_duplicates',
            'schedule': 300.0,
        }
    },
    beat_scheduler='celery.beat:PersistentScheduler',
    beat_schedule_filename='/tmp/celery/celerybeat-schedule',
    beat_sync_every=0,
    beat_max_loop_interval=300
)

# Update Redis initialization
def init_redis_queues():
    """Initialize Redis queues with proper formats."""
    try:
        redis_client = redis.Redis.from_url(
            get_redis_url(),
            decode_responses=True,
            socket_timeout=5,
            retry_on_timeout=True
        )
        
        # Don't clear everything by default
        if os.getenv('REDIS_CLEAR_ON_START', 'false').lower() == 'true':
            redis_client.flushall()

        # Create message format
        init_message = {
            "body": "",
            "content-type": "application/json",
            "content-encoding": "utf-8",
            "properties": {
                "delivery_tag": "init",
                "delivery_mode": 2,
                "delivery_info": {
                    "exchange": "",
                    "routing_key": ""
                },
                "priority": 0,
                "body_encoding": "base64",
                "correlation_id": None,
                "reply_to": None
            },
            "headers": {}
        }
        
        timestamp = float(datetime.now().timestamp())
        init_json = json.dumps(init_message)

        # Initialize keys with proper prefixes
        for key in ["celery:unacked", "celery:reserved", "celery:scheduled"]:
            redis_client.delete(key)
            redis_client.zadd(key, {init_json: timestamp})
            redis_client.zrem(key, init_json)

        # Initialize queue sets
        redis_client.sadd("celery:queues", "celery", "email_queue")
        
        logger.info("Redis queues initialized successfully")
        
    except Exception as e:
        logger.error(f"Failed to initialize Redis queues: {str(e)}")
        raise

# Move initialization to a function that can be called explicitly
def initialize():
    """Initialize Celery and Redis configurations"""
    init_redis_queues()

def get_test_delay():
    """Get delay time based on environment"""
    if os.getenv('TEST_MODE') == 'true':
        return int(os.getenv('TEST_DELAY', '60'))  # 1 minutes default
    return None

async def update_sequence_status(sequence_id: str):
    """Update sequence status based on audit records"""
    try:
        # Get all audit records for this sequence
        audits = list(sequence_audit_collection.find({"sequence_id": sequence_id}))
        
        if not audits:
            return
        
        # Check if all audits are completed or failed
        all_completed = all(audit["status"] in ["SENT", "FAILED", "CANCELLED"] for audit in audits)
        any_failed = any(audit["status"] in ["FAILED", "CANCELLED"] for audit in audits)
        
        new_status = "COMPLETED" if all_completed and not any_failed else \
                    "FAILED" if all_completed and any_failed else \
                    "IN_PROGRESS"

        # Update sequence status
        sequence_collection.update_one(
            {"_id": ObjectId(sequence_id)},
            {
                "$set": {
                    "status": new_status,
                    "updated_at": datetime.utcnow()
                }
            }
        )
        logger.info(f"Updated sequence {sequence_id} status to {new_status}")

    except Exception as e:
        logger.error(f"Error updating sequence status: {str(e)}")

@celery_app.task(name='cleanup_test_duplicates', shared=True)
def cleanup_test_duplicates():
    """Clean up duplicate test mode entries"""
    try:
        # Find sequences with test mode duplicates
        pipeline = [
            {
                "$group": {
                    "_id": {
                        "sequence_id": "$sequence_id",
                        "step_index": "$step_index"
                    },
                    "count": {"$sum": 1},
                    "docs": {"$push": "$$ROOT"}
                }
            },
            {
                "$match": {
                    "count": {"$gt": 1}
                }
            }
        ]

        duplicates = sequence_audit_collection.aggregate(pipeline)

        for duplicate in duplicates:
            docs = sorted(duplicate["docs"], key=lambda x: x["created_at"], reverse=True)
            kept_doc = docs[0]

            # Update other docs to cancelled
            for doc in docs[1:]:
                sequence_audit_collection.update_one(
                    {"_id": doc["_id"]},
                    {
                        "$set": {
                            "status": "CANCELLED",
                            "error_message": "Duplicate test mode entry",
                            "updated_at": datetime.utcnow()
                        }
                    }
                )

            # Update sequence status synchronously since we're in a Celery task
            if kept_doc.get("sequence_id"):
                update_sequence_status_sync(kept_doc["sequence_id"])

    except Exception as e:
        logger.error(f"Error cleaning up test duplicates: {str(e)}")

def update_sequence_status_sync(sequence_id: str):
    """Synchronous version of update_sequence_status for Celery tasks"""
    try:
        audits = list(sequence_audit_collection.find({"sequence_id": sequence_id}))
        if not audits:
            return
        
        all_completed = all(audit["status"] in ["SENT", "FAILED", "CANCELLED"] for audit in audits)
        any_failed = any(audit["status"] in ["FAILED", "CANCELLED"] for audit in audits)
        
        new_status = "COMPLETED" if all_completed and not any_failed else \
                    "FAILED" if all_completed and any_failed else \
                    "IN_PROGRESS"

        sequence_collection.update_one(
            {"_id": ObjectId(sequence_id)},
            {
                "$set": {
                    "status": new_status,
                    "updated_at": datetime.utcnow()
                }
            }
        )
        logger.info(f"Updated sequence {sequence_id} status to {new_status}")
    except Exception as e:
        logger.error(f"Error updating sequence status: {str(e)}")

@celery_app.task(
    bind=True, 
    name='send_scheduled_email',
    queue='email_queue',
    routing_key='email.send',
    shared=True
)
def send_scheduled_email(self, email_payload: dict, scheduled_time: str = None, token_data: dict = None, is_test_mode: bool = False):
    """Celery task for sending scheduled emails."""
    try:
        logger.info(f"Processing email task with payload: {email_payload}")
        
        # Move content to body if needed
        if 'content' in email_payload and 'body' not in email_payload:
            email_payload['body'] = email_payload.pop('content')

        logger.info(f"Token data present: {bool(token_data)}")
        logger.info(f"Is test mode: {is_test_mode}")
        
        # Handle test mode
        if not is_test_mode and os.getenv('TEST_MODE') == 'true':
            test_delay = int(os.getenv('TEST_DELAY', '60'))
            eta = datetime.utcnow() + timedelta(seconds=test_delay)
            
            new_task = self.apply_async(
                kwargs={
                    'email_payload': email_payload,
                    'token_data': token_data,
                    'is_test_mode': True
                },
                eta=eta,
                queue='email_queue',
                routing_key='email.send'
            )
            return {"status": "delayed", "task_id": new_task.id}
        
        # Send email
        if token_data:
            from talentwizer_commons.utils.email import send_email_from_user_email, EmailPayload
            
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            try:
                email_result = loop.run_until_complete(
                    send_email_from_user_email(token_data, EmailPayload(**email_payload))
                )
                
                # Update audit record
                audit = sequence_audit_collection.find_one_and_update(
                    {"schedule_id": self.request.id},
                    {
                        "$set": {
                            "status": "SENT",
                            "sent_time": datetime.utcnow(),
                            "updated_at": datetime.utcnow()
                        }
                    },
                    return_document=True
                )

                # Update sequence status using sync version
                if audit and audit.get("sequence_id"):
                    update_sequence_status_sync(audit["sequence_id"])

                return {
                    "status": "sent",
                    "result": email_result,
                    "sent_time": datetime.utcnow().isoformat()
                }
            finally:
                loop.close()
        else:
            raise ValueError("Token data required to send email")
            
    except Exception as e:
        logger.error(f"Error in send_scheduled_email: {str(e)}", exc_info=True)
        # Update audit record on failure
        sequence_audit_collection.update_one(
            {"schedule_id": self.request.id},
            {
                "$set": {
                    "status": "FAILED",
                    "error_message": str(e),
                    "updated_at": datetime.utcnow()
                }
            }
        )
        raise

# Use a simpler singleton pattern
_task_restore_complete = False

@celery_app.task(bind=True, name='restore_persisted_tasks')
def restore_persisted_tasks(self):
    """Task to restore persisted tasks on worker startup."""
    global _task_restore_complete
    
    if _task_restore_complete:
        logger.info("Tasks already restored, skipping...")
        return 0

    try:
        from .task_restore import restore_tasks
        result = restore_tasks()
        _task_restore_complete = True
        return result
    except Exception as e:
        logger.error(f"Task restoration failed: {str(e)}")
        return 0

@worker_ready.connect
def on_worker_ready(sender, **kwargs):
    """Run task restoration exactly once when worker is ready."""
    global _task_restore_complete
    if not _task_restore_complete:
        restore_persisted_tasks.apply_async(countdown=5)

# Add logger setup
@after_setup_logger.connect
def setup_loggers(logger, *args, **kwargs):
    """Configure logging for Celery."""
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    # Add your logging configuration here if needed

# Add task event handlers
@task_sent.connect
def task_sent_handler(sender=None, headers=None, body=None, **kwargs):
    """Handle task sent event."""
    task_id = headers.get('id') if headers else None
    if task_id:
        try:
            redis_client = redis.Redis.from_url(get_redis_url())
            redis_client.set(
                f'flower:task:{task_id}',
                json.dumps({
                    'status': PENDING,
                    'sent': datetime.utcnow().isoformat()
                }),
                ex=86400
            )
        except Exception as e:
            logger.error(f"Error in task_sent_handler: {str(e)}")
        finally:
            redis_client.close() if 'redis_client' in locals() else None

@task_received.connect
def task_received_handler(sender=None, request=None, **kwargs):
    """Handle task received event."""
    if request and request.id:
        try:
            redis_client = redis.Redis.from_url(get_redis_url())
            redis_client.set(
                f'flower:task:{request.id}',
                json.dumps({
                    'status': PENDING,
                    'received': datetime.utcnow().isoformat()
                }),
                ex=86400
            )
        except Exception as e:
            logger.error(f"Error in task_received_handler: {str(e)}")
        finally:
            redis_client.close() if 'redis_client' in locals() else None

@task_success.connect
def task_success_handler(sender=None, result=None, **kwargs):
    """Handle task success event."""
    if sender and sender.request.id:
        try:
            redis_client = redis.Redis.from_url(get_redis_url())
            redis_client.set(
                f'flower:task:{sender.request.id}',
                json.dumps({
                    'status': SUCCESS,
                    'result': str(result),
                    'completed': datetime.utcnow().isoformat()
                }),
                ex=86400
            )
        except Exception as e:
            logger.error(f"Error in task_success_handler: {str(e)}")
        finally:
            redis_client.close() if 'redis_client' in locals() else None

@task_failure.connect
def task_failure_handler(sender=None, exception=None, **kwargs):
    """Handle task failure event."""
    if sender and sender.request.id:
        try:
            redis_client = redis.Redis.from_url(get_redis_url())
            redis_client.set(
                f'flower:task:{sender.request.id}',
                json.dumps({
                    'status': FAILURE,
                    'error': str(exception),
                    'failed': datetime.utcnow().isoformat()
                }),
                ex=86400
            )
        except Exception as e:
            logger.error(f"Error in task_failure_handler: {str(e)}")
        finally:
            redis_client.close() if 'redis_client' in locals() else None

if __name__ == '__main__':
    initialize()
    celery_app.start()