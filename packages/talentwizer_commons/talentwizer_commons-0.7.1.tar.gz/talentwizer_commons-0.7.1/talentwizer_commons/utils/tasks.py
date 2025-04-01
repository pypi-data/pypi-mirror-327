from .celery_init import celery_app

# Import tasks after celery_app to avoid circular imports
from .celery_init import (
    send_scheduled_email,
    cleanup_test_duplicates,
    update_sequence_status_sync,
    restore_persisted_tasks  # Add this import
)

__all__ = [
    'celery_app',
    'send_scheduled_email',
    'cleanup_test_duplicates',
    'update_sequence_status_sync',
    'restore_persisted_tasks'  # Add this to __all__
]
