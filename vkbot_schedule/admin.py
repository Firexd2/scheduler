from django.contrib import admin

from vkbot_schedule.models import *

admin.site.register(ScheduleEveryDay)
admin.site.register(TimesForEveryDay)
admin.site.register(ScheduleEveryWeek)
admin.site.register(ScheduleEveryMonth)
admin.site.register(ScheduleEveryYear)
admin.site.register(ScheduleDay)
admin.site.register(ReplyMessages)
