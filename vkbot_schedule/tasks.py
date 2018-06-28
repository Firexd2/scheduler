from celery.schedules import crontab
from celery.task import periodic_task

from Celery import app
from vkbot_schedule.checks import *
from vkbot_schedule.message_handler import send_message


@periodic_task(run_every=crontab(minute='*/1'))
def schedule_every_minute():
    subtask_every_day.delay()
    subtask_every_week.delay()
    subtask_every_month.delay()
    subtask_every_year.delay()
    subtask_day.delay()


@app.task
def subtask_every_day():
    for uid, message in check_every_day():
        send_message(uid, message)


@app.task
def subtask_every_week():
    for uid, message in check_every_week():
        send_message(uid, message)


@app.task
def subtask_every_month():
    for uid, message in check_every_month():
        send_message(uid, message)


@app.task
def subtask_every_year():
    for uid, message in check_every_year():
        send_message(uid, message)


@app.task
def subtask_day():
    for uid, message in check_day():
        send_message(uid, message)
