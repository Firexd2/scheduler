from vkbot_schedule.models import *
import datetime
import re
from pytz import timezone


def query_analyzer_every_day(query, uid):
    """
    Считаем, что нам пришел правильный запрос в виде
    >> !каждыйдень <название> <10:00,13:00,15:00> <сообщение> 4

    Создаем задание в БД
    """
    list_query = query.split(' ') # сохраняеи запрос в виде списка через пробел

    times = list_query[2].split(',') # разбиваем времена через запятую

    repeat = int(list_query[-1]) if len(list_query) == 5 else 1  # Сколько раз повторять?

    instance_times = [] # необходимые экземпляры для сохранения

    message = (' ').join(list_query[3].split('-')) # сообщение наше за место пробелов дефисы

    # Сохраняем время и запоминаем экземпляры для создания связи
    for time in times:
        inst = TimesForEveryDay(time=time, repeat_count=repeat)
        inst.save()
        instance_times.append(inst)

    # Создаем задание в базе данных
    sed = ScheduleEveryDay(uid=uid, name=list_query[1], message=message)
    sed.save()

    # сохраняем ранее созданые экземпляры времён в наш экземлпяр задания
    for time in instance_times:
        sed.times.add(time)


def query_analyzer_every_week(query, uid):
    """
    Считаем, что нам пришел правильный запрос в виде
    >> !каждуюнеделю <название> <пн,ср,пт> <сообщение>

    Создаем задание в БД
    """
    list_query = query.split(' ') # сохраняеи запрос в виде списка через пробел
    message = (' ').join(list_query[3].split('-')) # сообщение наше за место пробелов дефисы

    ScheduleEveryWeek(uid=uid, name=list_query[1], week_day=list_query[2], message=message).save()


def query_analyzer_every_year(query, uid):
    """
    Считаем, что нам пришел правильный запрос в виде
    >> !каждыйгод <название> <24.01> <сообщение>

    Создаем задание в БД
    """
    list_query = query.split(' ') # сохраняеи запрос в виде списка через пробел
    message = (' ').join(list_query[3].split('-')) # сообщение наше за место пробелов дефисы

    ScheduleEveryYear(uid=uid, name=list_query[1], day=list_query[2], message=message).save()


def query_analyzer_day(query, uid):
    """
    Считаем, что нам пришел правильный запрос в виде
    >> !день <название> <01.02.2018-10:30> <сообщение>

    Создаем задание в БД
    """
    list_query = query.split(' ') # сохраняеи запрос в виде списка через пробел

    v = list(map(int, re.split('[.\\-:]', list_query[2]))) # получаем [01, 02, 2018, 10, 30]

    tz = timezone('Europe/Moscow') # Московкий пояс
    date_time = datetime.datetime(v[2], v[1], v[0], v[3], v[4], tzinfo=tz) # получаем экземлпяр даты и времени

    message = (' ').join(list_query[3].split('-')) # сообщение наше за место пробелов дефисы

    ScheduleDay(uid=uid, name=list_query[1], day=date_time, message=message).save()






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


