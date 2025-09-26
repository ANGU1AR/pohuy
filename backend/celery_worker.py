from main import celery, app as fastapi_app
from celery.schedules import crontab

# Example task for processing 176k
@celery.task
def process_batch(tasks):
    # Logic for batch
    pass

celery.conf.beat_schedule = {
    'monthly-process': {
        'task': 'celery_worker.process_batch',
        'schedule': crontab(day_of_month='1,15'),  # 2x/month
    },
}