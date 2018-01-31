from datetime import *
from vkbot_schedule.filters import *
from vkbot_schedule.models import *


def command_analyzer(query, uid):

    list_query = query.split(' ') # сохраняеи запрос в виде списка через пробел
    command = list_query[0].lower()
    q = list_query[1:]

    dict_command = {'!каждыйдень': query_analyzer_every_day,
                    '!кд': query_analyzer_every_day,
                    '!каждуюнеделю': query_analyzer_every_week,
                    '!кн': query_analyzer_every_week,
                    '!каждыймесяц': query_analyzer_every_month,
                    '!км': query_analyzer_every_month,
                    '!каждыйгод': query_analyzer_every_year,
                    '!кг': query_analyzer_every_year,
                    '!день': query_analyzer_day,
                    '!д': query_analyzer_day}

    try:
        response = dict_command[command](q, uid)
    except KeyError:
        response = 'Такой команды не существует'
    except Exception as error_message:
        response = error_message
    else:
        response = 'Команда успешно сохранена и активирована!' + response
    finally:
        return response


def actions_analyzer(query, uid):

    list_query = query.split(' ') # сохраняем запрос в виде списка через пробел
    action = list_query[0].lower()
    q = list_query[1:]

    dict_action = {
    }

    try:
        response = dict_action[action](uid, q[0])
    except KeyError:
        response = 'Такого действия не существует'
    finally:
        return response


def query_analyzer_every_day(query, uid):
    """
    Тест 10:00,13:00,15:00 Это-сообщение-прошу-повторить-мне
    """
    response_filter = filter_every_day(query)
    if response_filter:
        raise Exception(response_filter)

    times = query[1].split(',') # разбиваем времена через запятую
    instance_times = [] # необходимые экземпляры для сохранения
    message = (' ').join(query[2].split('-')) # сообщение наше за место пробелов дефисы

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

    message = (' ').join(query[3].split('-')) # сообщение наше за место пробелов дефисы
    ScheduleEveryWeek(uid=uid, name=query[0], week_day=query[1], message=message,
                      time=query[2], date=datetime.now().date() - timedelta(days=1)).save()

    return 'Теперь я буду напоминать тебе в %s о твоей задаче!' % query[1]


def query_analyzer_every_month(query, uid):
    """
    Месяц 1,5,8,26 9:30 Напоминаем-о-молочке
    """
    response_filter = filter_every_month(query)
    if response_filter:
        raise Exception(response_filter)

    message = (' ').join(query[3].split('-')) # сообщение наше за место пробелов дефисы
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

    message = (' ').join(query[3].split('-')) # сообщение наше за место пробелов дефисы
    ScheduleEveryYear(uid=uid, name=query[0], day=query[1],
                      message=message, time=query[2], date=datetime.now().date() - timedelta(days=1)).save()

    return 'Теперь я буду напоминать тебе о твоей задаче %s ежегодно!' % query[1]


def query_analyzer_day(query, uid):

    response_filter = filter_day(query)
    if response_filter:
        raise Exception(response_filter)

    message = (' ').join(query[2].split('-')) # сообщение наше за место пробелов дефисы
    ScheduleDay(uid=uid, name=query[0], day=query[1], message=message).save()

    return 'Теперь я напомню о твоей задаче %s.' % query[1]
