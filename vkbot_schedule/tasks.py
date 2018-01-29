from celery.schedules import crontab
from celery.task import periodic_task
from vkbot_schedule.checks import *
from vkbot_schedule.message_handler import send_message


@periodic_task(run_every=crontab(minute='*/2'))
def schedule_every_day_task():
    """
    Эта функция будет выполняться каждые пять минут для проверки задания.
    Если текущее время больше, чем в время указанное в задании, и это время не 'подтверждено',
    то отсылаем сообщение пользователю о том, что надо выполнить задание.
    """
    for uid, message in check_every_day():
        send_message(uid, message)


@periodic_task(run_every=crontab(minute=0, hour=9))
def schedule_every_week_task():
    """
    Это задание будет выполнятся каждый день для проверки еженедельных команд
    """

    for uid, message in check_every_week():
        send_message(uid, message)


@periodic_task(run_every=crontab(minute=0, hour=9))
def schedule_every_month_task():
    """
    Это задание будет выполняться каждый месяц по определенным дням 
    """
    for uid, message in check_every_month():
        send_message(uid, message)


@periodic_task(run_every=crontab(minute=0, hour=9))
def schedule_every_year_task():
    """
    Это задание будет выполнятся каждый день для проверки и выполнения ежегодного задания
    """
    for uid, message in check_every_year():
        send_message(uid, message)


@periodic_task(run_every=crontab(minute='*/2'))
def schedule_day_task():
    for uid, message in check_day():
        send_message(uid, message)
