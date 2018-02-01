from datetime import datetime
from django.db import models


class TimesForEveryDay(models.Model):
    time = models.CharField(max_length=5)
    date = models.DateField(default=datetime.now, blank=True)

    class Meta:
        verbose_name = 'Времена для !каждыйдень'
        verbose_name_plural = 'Времена для !каждыйдень'


class ScheduleEveryDay(models.Model):
    uid = models.IntegerField()
    name = models.CharField(max_length=100)
    message = models.CharField(max_length=100)
    times = models.ManyToManyField(TimesForEveryDay)

    def __str__(self):
        return 'Тип: !каждыйдень, название: %s, время: %s, сообщение: %s' %\
               (self.name, " ".join([time.time for time in self.times.all()]), self.message)

    def __repr__(self):
        return 'Тип: !каждыйдень, название: %s, время: %s, сообщение: %s' %\
               (self.name, " ".join([time.time for time in self.times.all()]), self.message)

    class Meta:
        verbose_name = 'Расписание на !каждыйдень'
        verbose_name_plural = 'Расписания на !каждыйдень'


# Еженедельные задания
class ScheduleEveryWeek(models.Model):
    uid = models.IntegerField()
    name = models.CharField(max_length=100)
    message = models.CharField(max_length=100)
    week_day = models.CharField(max_length=20)
    time = models.CharField(max_length=5)
    date = models.DateField(default=datetime.now, blank=True)

    def __str__(self):
        return 'Тип: !каждуюнеделю, название: %s, дни недели: %s, время: %s, сообщение: %s' %\
               (self.name, self.week_day, self.time, self.message)

    def __repr__(self):
        return 'Тип: !каждуюнеделю, название: %s, дни недели: %s, время: %s, сообщение: %s' %\
               (self.name, self.week_day, self.time, self.message)

    class Meta:
        verbose_name = 'Расписание на !каждуюнеделю'
        verbose_name_plural = 'Расписания на !каждуюнеделю'


class ScheduleEveryMonth(models.Model):
    uid = models.IntegerField()
    name = models.CharField(max_length=100)
    message = models.CharField(max_length=100)
    days = models.CharField(max_length=60)
    time = models.CharField(max_length=5)
    date = models.DateField(default=datetime.now, blank=True)

    def __str__(self):
        return 'Тип: !каждыймесяц, название: %s, числа: %s, время: %s, сообщение: %s' %\
               (self.name, self.days, self.time, self.message)

    def __repr__(self):
        return 'Тип: !каждыймесяц, название: %s, числа: %s, время: %s, сообщение: %s' %\
               (self.name, self.days, self.time, self.message)

    class Meta:
        verbose_name = 'Расписание на !каждыймесяц'
        verbose_name_plural = 'Расписания на !каждыймесяц'


class ScheduleEveryYear(models.Model):
    uid = models.IntegerField()
    name = models.CharField(max_length=100)
    message = models.CharField(max_length=100)
    day = models.CharField(max_length=5)
    time = models.CharField(max_length=5)
    date = models.DateField(default=datetime.now, blank=True)

    def __str__(self):
        return 'Тип: !каждыйгод, название: %s, день и месяц: %s, время: %s, сообщение: %s' %\
               (self.name, self.day, self.time, self.message)

    def __repr__(self):
        return 'Тип: !каждыйгод, название: %s, день и месяц: %s, время: %s, сообщение: %s' %\
               (self.name, self.day, self.time, self.message)

    class Meta:
        verbose_name = 'Расписание на !каждыйгод'
        verbose_name_plural = 'Расписания на !каждыйгод'


class ScheduleDay(models.Model):
    uid = models.IntegerField()
    name = models.CharField(max_length=100)
    message = models.CharField(max_length=100)
    day = models.CharField(max_length=16)

    def __str__(self):
        return 'Тип: !день, название: %s, дата и время: %s, сообщение: %s' %\
               (self.name, self.day, self.message)

    def __repr__(self):
        return 'Тип: !день, название: %s, дата и время: %s, сообщение: %s' %\
               (self.name, self.day, self.message)

    class Meta:
        verbose_name = 'Расписание на !день'
        verbose_name_plural = 'Расписания на !день'


class ReplyMessages(models.Model):
    message = models.CharField(max_length=600)
    answer = models.CharField(max_length=600)

    def __str__(self):
        return '%s' % self.message

    class Meta:
        verbose_name = 'Ответ на сообщения'
        verbose_name_plural = 'Ответы на сообщения'
