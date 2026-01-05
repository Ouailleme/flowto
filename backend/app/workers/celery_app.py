"""Celery application configuration"""
from celery import Celery
from app.config import settings

# Create Celery app
celery_app = Celery(
    "financeai",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=[
        "app.workers.tasks",
    ]
)

# Configure Celery
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    task_soft_time_limit=25 * 60,  # 25 minutes (warning)
    worker_prefetch_multiplier=4,
    worker_max_tasks_per_child=1000,
)

# Beat schedule (periodic tasks)
celery_app.conf.beat_schedule = {
    # Categorize uncategorized transactions every hour
    "categorize-transactions-hourly": {
        "task": "app.workers.tasks.categorize_uncategorized_transactions_task",
        "schedule": 3600.0,  # Every hour
    },
    # Process overdue invoices (send reminders) daily at 9am
    "process-overdue-invoices-daily": {
        "task": "app.workers.tasks.process_overdue_invoices_task",
        "schedule": {
            "hour": 9,
            "minute": 0,
        },
    },
    # Sync bank transactions every 6 hours
    "sync-bank-transactions": {
        "task": "app.workers.tasks.sync_all_bank_accounts_task",
        "schedule": 21600.0,  # Every 6 hours
    },
}


