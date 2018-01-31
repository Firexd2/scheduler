import re
from vkbot_schedule.models import *


def check_every_day():
    now = datetime.now()
    now_time = now.time().strftime("%H:%M") # текущее время
    for item in ScheduleEveryDay.objects.all(): # цикл обхода всех заданий в базе
        for time in item.times.all(): # проверка времени в задании
            if now_time >= time.time and time.date != now.date():
                time.save(update_fields=['date'])
                yield (item.uid, item.message)


def check_every_week():
    days_of_week = {'пн': 1, 'вт': 2, 'ср': 3, 'чт': 4, 'пт': 5, 'сб': 6, 'вс': 7}
    now = datetime.now()
    now_day = now.isoweekday() # получение номера текущего дня
    now_time = now.time().strftime("%H:%M") # текущее время
    for item in ScheduleEveryWeek.objects.all():
        for day in item.week_day.split(','):
            if days_of_week[day] == now_day and now_time >= item.time and item.date != now.date():
                item.save(update_fields=['date'])
                yield (item.uid, item.message)


def check_every_month():
    now = datetime.now()
    now_time = now.time().strftime("%H:%M") # текущее время
    now_day = now.day
    for item in ScheduleEveryMonth.objects.all():
        for day in item.days.split(','):
            if int(day) == now_day and now_time >= item.time and item.date != now.date():
                item.save(update_fields=['date'])
                yield (item.uid, item.message)


def check_every_year():
    now = datetime.now()
    now_time = now.time().strftime("%H:%M") # текущее время
    now_day = now.strftime('%d.%m') # текущая дата
    for item in ScheduleEveryYear.objects.all():
        if item.day == now_day and now_time >= item.time and item.date != now.date():
            item.save(update_fields=['date'])
            yield (item.uid, item.message)


def check_day():
    now_datetime = datetime.now()
    for item in ScheduleDay.objects.all():
        v = list(map(int, re.split('[.\\-:]', item.day)))  # получаем [01, 02, 2018, 10, 30]
        date_time = datetime(v[2], v[1], v[0], v[3], v[4])  # получаем экземлпяр даты и времени
        if date_time <= now_datetime:
            yield (item.uid, item.message)
            item.delete()
