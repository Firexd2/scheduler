from vkbot_schedule.models import *

ALL_SCHEDULE = [ScheduleEveryDay, ScheduleEveryWeek, ScheduleEveryMonth, ScheduleEveryYear, ScheduleDay]


def actions_delete_schedule(query, uid):
    """
    Тест
    """
    if len(query) == 0:
        raise Exception('Вы не ввели название расписания для удаления. Необходимо ввести в формате @у Название.')
    name_command = query[0]
    n = 0
    for schedule in ALL_SCHEDULE:
        n += schedule.objects.filter(uid=uid, name=name_command).delete()[0]

    if n:
        return 'Расписания в количестве %s, с названием "%s", удалены.' % (n, name_command)
    else:
        return 'Расписаний с названием "%s" у тебя нет.' % name_command


def actions_all_schedule(query, uid):
    answer = ''

    for schedule in ALL_SCHEDULE:
        for command in schedule.objects.filter(uid=uid):
            answer += '-%s\n\n' % str(command)

    if answer:
        return 'Cписок твоих расписаний:\n\n\n' + answer
    else:
        return 'Ты не задавал никаких расписаний'
