from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor
from django.core.management import call_command

def start():
    executors = {
        'default': ThreadPoolExecutor(1)
    }
    scheduler = BackgroundScheduler(executors=executors)
    scheduler.add_job(
        lambda: call_command('release_vehicles'),
        'interval',
        minutes=1
    )
    scheduler.start()