from apscheduler.schedulers.blocking import BlockingScheduler
from app.main import get_crypto_from_database_with_details, get_amount
from app.db import insert_amount_in_database

sched = BlockingScheduler()

@sched.scheduled_job('cron', day_of_week='mon-fri', hour=5, minute=5)
def scheduled_job():
    cryptomonaies = get_crypto_from_database_with_details()
    amount = get_amount(cryptomonaies)
    insert_amount_in_database(amount)
sched.start()
