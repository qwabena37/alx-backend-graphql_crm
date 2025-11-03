Instructions:

1. Set Up Celery:

    Add celery and django-celery-beat to requirements.txt.
    Add django_celery_beat to INSTALLED_APPS in crm/settings.py.
    Create crm/celery.py to initialize the Celery app with Redis as the broker (redis://localhost:6379/0).
    Update crm/__init__.py to load the Celery app.

2. Define the Celery Task:

    In crm/tasks.py, define a task generate_crm_report that:
    Uses a GraphQL query to fetch: * Total number of customers. * Total number of orders. * Total revenue (sum of totalamount from orders).
    Logs the report to/tmp/crm_report_log.txt with a timestamp in the format YYYY-MM-DD HH:MM:SS - Report: X customers, Y orders, Z revenue.

3. Schedule with Celery Beat:

    In crm/settings.py, configure:

CELERY_BEAT_SCHEDULE = {
    'generate-crm-report': {
        'task': 'crm.tasks.generate_crm_report',
        'schedule': crontab(day_of_week='mon', hour=6, minute=0),
    },
}

4. Document Setup:

Create crm/README.md with steps to:

    InstallRedis and dependencies.
    Run migrations (python manage.py migrate).
    Start Celery worker (celery -A crm worker -l info).
    Start Celery Beat (celery -A crm beat -l info).
    Verify logs in /tmp/crm_report_log.txt.
