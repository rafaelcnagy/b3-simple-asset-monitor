from apscheduler.schedulers.background import BackgroundScheduler
from monitoring.api import API

def start():
    scheduler = BackgroundScheduler(timezone='America/Sao_Paulo')
    api = API()
    scheduler.add_job(
        api.update_data,
        'interval',
        minutes=60,
    )
    scheduler.add_job(
        api.update_all_data,
        'cron',
        hour=6,
        minute=0,
    )
    scheduler.start()
