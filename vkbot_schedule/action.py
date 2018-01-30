from vkbot_schedule.models import *


def answer_done(uid, name_schedule):
    """
    Эта функция будет обрабатывать подтвреждение выполнения задания.
    На вход приходит uid пользователя и название задания
    Если данные верны, то функция запишет в первом времени done в True
    """

    command = ScheduleEveryDay.objects.get(uid=uid, name=name_schedule)

    for time in command.times.all():
        if not time.repeat_count:
            time.repeat_count = 0
            time.save()
            return 'Твое выполнение зафиксировано'
