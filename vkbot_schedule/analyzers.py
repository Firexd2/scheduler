from datetime import *
from vkbot_schedule.filters import *
from vkbot_schedule.models import *


def query_analyzer_every_day(query, uid):
    """
    Тест 10:00,13:00,15:00 Это-сообщение-прошу-повторить-мне
    """
    response_filter = filter_every_day(query)
    if response_filter:
        raise Exception(response_filter)

    times = query[1].split(',')
    instance_times = []

    message = ' '.join(query[2].split('-'))

    # Сохраняем время и запоминаем экземпляры для создания связи
    for t in times:
        inst = TimesForEveryDay(time=t, date=datetime.now().date() - timedelta(days=1))
        inst.save()
        instance_times.append(inst)

    # Создаем задание в базе данных
    sed = ScheduleEveryDay(uid=uid, name=query[0], message=message)
    sed.save()

    # сохраняем ранее созданые экземпляры времён в наш экземлпяр задания
    for t in instance_times:
        sed.times.add(t)

    return 'Теперь я буду напоминать тебе о твоей задаче ежедневно в %s!' % query[1]


def query_analyzer_every_week(query, uid):
    """
    Тест пн,ср,пт 10:30 Это-задание,-повторяем-,каждую-неделю-в-10:30
    """
    response_filter = filter_every_week(query)
    if response_filter:
        raise Exception(response_filter)

    message = ' '.join(query[3].split('-'))
    ScheduleEveryWeek(uid=uid, name=query[0], week_day=query[1], message=message,
                      time=query[2], date=datetime.now().date() - timedelta(days=1)).save()

    return 'Теперь я буду напоминать тебе о твоей задаче по %s в %s!' % (query[1], query[2])


def query_analyzer_every_month(query, uid):
    """
    Месяц 1,5,8,26 9:30 Напоминаем-о-молочке
    """
    response_filter = filter_every_month(query)
    if response_filter:
        raise Exception(response_filter)

    message = ' '.join(query[3].split('-'))
    ScheduleEveryMonth(uid=uid, name=query[0], days=query[1], message=message,
                       time=query[2], date=datetime.now().date() - timedelta(days=1)).save()

    return 'Теперь я буду напоминать тебе о твоей задаче по %s числам ежемесячно!' % query[1]


def query_analyzer_every_year(query, uid):
    """
    Год 24.01 09:00 Повторяем-каждый-год
    """
    response_filter = filter_every_year(query)
    if response_filter:
        raise Exception(response_filter)

    message = ' '.join(query[3].split('-'))
    ScheduleEveryYear(uid=uid, name=query[0], day=query[1],
                      message=message, time=query[2], date=datetime.now().date() - timedelta(days=1)).save()

    return 'Теперь я буду напоминать тебе о твоей задаче %s ежегодно!' % query[1]


def query_analyzer_day(query, uid):

    response_filter = filter_day(query)
    if response_filter:
        raise Exception(response_filter)

    if query[1][:7] == 'Сегодня':
        query[1] = datetime.now().date().strftime('%d.%m.%Y') + query[7:]
    if query[1][:6] == 'Завтра':
        query[1] = (datetime.now() + timedelta(days=1)).date().strftime('%d.%m.%Y') + query[6:]

    message = ' '.join(query[2].split('-'))
    ScheduleDay(uid=uid, name=query[0], day=query[1], message=message).save()

    return 'Теперь я напомню о твоей задаче %s.' % query[1]
