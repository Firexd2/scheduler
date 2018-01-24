from django.db import models


# Времена для ежедневных заданий
class TimesForEveryDay(models.Model):
    time = models.CharField(max_length=5)
    repeat_count = models.IntegerField()


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


# Ежегодные задания
class ScheduleEveryYear(models.Model):
    uid = models.IntegerField()
    name = models.CharField(max_length=100)
    message = models.CharField(max_length=100)
    day = models.CharField(max_length=5)


# Разовые задания в определенное время
class ScheduleDay(models.Model):
    uid = models.IntegerField()
    name = models.CharField(max_length=100)
    message = models.CharField(max_length=100)
    day = models.DateTimeField()
