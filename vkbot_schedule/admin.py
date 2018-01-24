from django.contrib import admin

from vkbot_schedule.models import ScheduleEveryDay, TimesForEveryDay

admin.site.register(ScheduleEveryDay)

admin.site.register(TimesForEveryDay)