from django.db import models


# Времена для ежедневных заданий
class TimesForEveryDay(models.Model):
    time = models.CharField(max_length=5)
    date = models.DateField(auto_now=True)


# Ежедневные задания
class ScheduleEveryDay(models.Model):
    uid = models.IntegerField()
    name = models.CharField(max_length=100)
    message = models.CharField(max_length=100)
    times = models.ManyToManyField(TimesForEveryDay)


# Еженедельные задания
class ScheduleEveryWeek(models.Model):
    uid = models.IntegerField()
    name = models.CharField(max_length=100)
    message = models.CharField(max_length=100)
    week_day = models.CharField(max_length=20)
    time = models.CharField(max_length=5)
    date = models.DateField(auto_now=True)


# Ежемесячные задания
class ScheduleEveryMonth(models.Model):
    uid = models.IntegerField()
    name = models.CharField(max_length=100)
    message = models.CharField(max_length=100)
    days = models.CharField(max_length=60)
    time = models.CharField(max_length=5)
    date = models.DateField(auto_now=True)


# Ежегодные задания
class ScheduleEveryYear(models.Model):
    uid = models.IntegerField()
    name = models.CharField(max_length=100)
    message = models.CharField(max_length=100)
    day = models.CharField(max_length=5)
    time = models.CharField(max_length=5)
    date = models.DateField(auto_now=True)


# Разовые задания в определенное время
class ScheduleDay(models.Model):
    uid = models.IntegerField()
    name = models.CharField(max_length=100)
    message = models.CharField(max_length=100)
    day = models.CharField(max_length=16)
