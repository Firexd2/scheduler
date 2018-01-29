from celery.schedules import crontab
from celery.task import periodic_task
from vkbot_schedule.checks import *
from vkbot_schedule.message_handler import send_message


@periodic_task(run_every=crontab())
def schedule_every_minute():
    tasks = [check_every_day(), check_day()]
    for task in tasks:
        for uid, message in task:
            send_message(uid, message)


@periodic_task(run_every=crontab(minute=0, hour=9))
def schedule_every_day():
    tasks = [check_every_week(), check_every_month(), check_every_year()]
    for task in tasks:
        for uid, message in task:
            send_message(uid, message)
