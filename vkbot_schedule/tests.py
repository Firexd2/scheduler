from datetime import timedelta

from django.test import TestCase

from vkbot_schedule.checks import *
from .analyzers import *


class TestQueryAnalyzeres(TestCase):

    def test_analyzer_every_day(self):
        query = '!каждыйдень Тест 10:00,13:00,15:00 Это-сообщение-прошу-повторить-мне'
        command_analyzer(query, 123)

        r = ScheduleEveryDay.objects.get(id=1)

        self.assertEqual(r.uid, 123)
        self.assertEqual(r.name, 'Тест')
        self.assertEqual(r.message, 'Это сообщение прошу повторить мне')

        all_times = r.times.all()
        self.assertTrue(len(all_times) == 3)

        self.assertEqual(all_times[0].time, '10:00')
        self.assertEqual(all_times[1].time, '13:00')
        self.assertEqual(all_times[2].time, '15:00')

    def test_analyzer_every_week(self):
        query = '!каждуюНеделю Тест пн,ср,пт 10:30 Это-задание,-повторяем-,каждую-неделю'
        command_analyzer(query, 123)

        r = ScheduleEveryWeek.objects.get(id=1)

        self.assertEqual(r.uid, 123)
        self.assertEqual(r.name, 'Тест')
        self.assertEqual(r.time, '10:30')

        week_day = r.week_day.split(',')
        self.assertEqual(week_day[0], 'пн')
        self.assertEqual(week_day[1], 'ср')
        self.assertEqual(week_day[2], 'пт')

        self.assertEqual(r.message, 'Это задание, повторяем ,каждую неделю')

    def test_analyzer_every_month(self):
        query = '!Каждыймесяц Месяц 1,5,8,26 10:30 Напоминаем-о-молочке'
        command_analyzer(query, 123)

        r = ScheduleEveryMonth.objects.get(id=1)

        self.assertEqual(r.uid, 123)
        self.assertEqual(r.name, 'Месяц')
        self.assertEqual(r.time, '10:30')
        self.assertEqual(r.message, 'Напоминаем о молочке')
        self.assertEqual(r.days, '1,5,8,26')

    def test_analyzer_every_year(self):
        query = '!каждыйгод Год 24.01 9:00 Повторяем-каждый-год'
        command_analyzer(query, 123)

        r = ScheduleEveryYear.objects.get(id=1)

        self.assertEqual(r.uid, 123)
        self.assertEqual(r.name, 'Год')
        self.assertEqual(r.time, '9:00')
        self.assertEqual(r.message, 'Повторяем каждый год')
        self.assertEqual(r.day, '24.01')

    def test_analyzer_day(self):
        query = '!дЕнь ДеньРождение 01.02.2018-10:50 Сегодня-день-рождение'
        command_analyzer(query, 123)

        r = ScheduleDay.objects.get(id=1)

        self.assertEqual(r.uid, 123)
        self.assertEqual(r.name, 'ДеньРождение')

        self.assertEqual(r.day, '01.02.2018-10:50')
        self.assertEqual(r.message, 'Сегодня день рождение')


class TestChecks(TestCase):

    def test_check_day(self):
        datetime_now = datetime.datetime.now()
        datetime_after = datetime_now - timedelta(minutes=3)
        datetime_before = datetime_now + timedelta(minutes=1)

        day_after = str(datetime_after.day) + '.' + str(datetime_after.month) + '.' + str(datetime_after.year) +\
                    '-' + str(datetime_after.hour) + ':' + str(datetime_after.minute)

        day_before = str(datetime_before.day) + '.' + str(datetime_before.month) + '.' + str(datetime_before.year) +\
                     '-' + str(datetime_before.hour) + ':' + str(datetime_before.minute)

        ScheduleDay(uid=1, name='Тест', day=day_after, message='ТЕСТ').save()
        ScheduleDay(uid=1, name='Тест2', day=day_before, message='ТЕСТ2').save()

        self.assertEqual(1, len([x for x in check_day()]))
