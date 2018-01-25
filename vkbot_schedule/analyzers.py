from vkbot_schedule.models import *
import datetime
import re
from pytz import timezone


def query_analyzer_common(query, uid):

    list_query = query.split(' ') # сохраняеи запрос в виде списка через пробел
    command = list_query[0].lower()

    if command == '!каждыйдень':
        query_analyzer_every_day(list_query[1:], uid)
    elif command == '!каждуюнеделю':
        query_analyzer_every_week(list_query[1:], uid)
    elif command == '!каждыймесяц':
        query_analyzer_every_month(list_query[1:], uid)
    elif command == '!каждыйгод':
        query_analyzer_every_year(list_query[1:], uid)
    elif command == '!день':
        query_analyzer_day(list_query[1:], uid)


def query_analyzer_every_day(query, uid):

    times = query[1].split(',') # разбиваем времена через запятую
    repeat = int(query[-1]) if len(query) == 4 else 1  # Сколько раз повторять?
    instance_times = [] # необходимые экземпляры для сохранения

    message = (' ').join(query[2].split('-')) # сообщение наше за место пробелов дефисы

    # Сохраняем время и запоминаем экземпляры для создания связи
    for time in times:
        inst = TimesForEveryDay(time=time, repeat_count=repeat)
        inst.save()
        instance_times.append(inst)

    # Создаем задание в базе данных
    sed = ScheduleEveryDay(uid=uid, name=query[0], message=message)
    sed.save()

    # сохраняем ранее созданые экземпляры времён в наш экземлпяр задания
    for time in instance_times:
        sed.times.add(time)


def query_analyzer_every_week(query, uid):
    message = (' ').join(query[2].split('-')) # сообщение наше за место пробелов дефисы
    ScheduleEveryWeek(uid=uid, name=query[0], week_day=query[1], message=message).save()


def query_analyzer_every_month(query, uid):
    message = (' ').join(query[2].split('-')) # сообщение наше за место пробелов дефисы
    ScheduleEveryMonth(uid=uid, name=query[0], days=query[1], message=message).save()


def query_analyzer_every_year(query, uid):
    message = (' ').join(query[2].split('-')) # сообщение наше за место пробелов дефисы
    ScheduleEveryYear(uid=uid, name=query[0], day=query[1], message=message).save()


def query_analyzer_day(query, uid):
    v = list(map(int, re.split('[.\\-:]', query[1]))) # получаем [01, 02, 2018, 10, 30]

    tz = timezone('Europe/Moscow') # Московкий пояс
    date_time = datetime.datetime(v[2], v[1], v[0], v[3], v[4], tzinfo=tz) # получаем экземлпяр даты и времени
    message = (' ').join(query[2].split('-')) # сообщение наше за место пробелов дефисы

    ScheduleDay(uid=uid, name=query[0], day=date_time, message=message).save()






def answer_done(uid, name_schedule):
    """
    Эта функция будет обрабатывать подтвреждение выполнения задания.
    На вход приходит uid пользователя и название задания
    Если данные верны, то функция запишет в первом времени done в True
    """
    try:
        command = ScheduleEveryDay.objects.get(uid=uid, name=name_schedule)
    except:
        return False

    for time in command.times.all():
        if not time.repeat_count:
            time.repeat_count = 0
            time.save()
            break


