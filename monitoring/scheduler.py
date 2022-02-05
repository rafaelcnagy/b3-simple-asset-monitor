from apscheduler.schedulers.background import BackgroundScheduler
from monitoring.api import API

def start():
    scheduler = BackgroundScheduler(timezone='America/Sao_Paulo')
    api = API()
    scheduler.add_job(
        api.update_data,
        'interval',
        minutes=30,
    )
    scheduler.start()
