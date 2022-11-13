import os

from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cheaters_project.settings')

app = Celery('cheaters_project')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')
task_serializer = "json"
result_serializer = "json"
accept_content = ["json"]

# Load task modules from all registered Django apps.
app.autodiscover_tasks()
