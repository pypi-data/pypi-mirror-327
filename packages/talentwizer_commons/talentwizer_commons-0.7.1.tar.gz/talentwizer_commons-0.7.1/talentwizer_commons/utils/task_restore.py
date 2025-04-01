import os
import redis
import logging
from datetime import datetime
import json
from .celery_init import send_scheduled_email
from .db import mongo_database

logger = logging.getLogger(__name__)

def restore_tasks():
    """Restore scheduled tasks from MongoDB and update Redis."""
    try:
        logger.info("Starting task restoration process...")
        
        redis_client = redis.Redis.from_url(
            os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0'),
            decode_responses=True,
            socket_timeout=5
        )
        
        # Get scheduled tasks from audit collection
        sequence_audit_collection = mongo_database["email_sequence_audits"]
        scheduled_tasks = sequence_audit_collection.find({
            "status": "SCHEDULED",
            "scheduled_time": {"$gt": datetime.utcnow()}
        })

        restored_count = 0
        for task in scheduled_tasks:
            try:
                task_id = task.get('schedule_id')
                if not task_id:
                    continue

                # Check if task is already in Redis
                if redis_client.exists(f"celery-task-meta-{task_id}"):
                    logger.info(f"Task {task_id} already exists, skipping...")
                    continue

                # Create task with exact same task_id
                task_args = {
                    'email_payload': task['email_payload'],
                    'scheduled_time': task['scheduled_time'].isoformat() if task.get('scheduled_time') else None,
                    'token_data': task.get('token_data')
                }

                # Schedule task with original ID
                new_task = send_scheduled_email.apply_async(
                    kwargs=task_args,
                    task_id=task_id,  # Use original task ID
                    eta=task.get('scheduled_time'),
                    queue='email_queue',
                    routing_key='email.send'
                )

                # Add task to Redis for Flower visibility
                task_meta = {
                    'status': 'PENDING',
                    'result': None,
                    'traceback': None,
                    'children': [],
                    'date_done': None,
                    'task_id': task_id
                }
                redis_client.set(
                    f"celery-task-meta-{task_id}",
                    json.dumps(task_meta),
                    ex=86400  # 24 hour expiry
                )

                logger.info(f"Restored task {task_id} with new task ID {new_task.id}")
                restored_count += 1

            except Exception as e:
                logger.error(f"Failed to restore task {task.get('schedule_id')}: {str(e)}")
                continue

        logger.info(f"Task restoration completed. Restored {restored_count} tasks")
        return restored_count

    except Exception as e:
        logger.error(f"Task restoration failed: {str(e)}")
        return 0
