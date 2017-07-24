from django.contrib import admin

from .models import *

admin.site.register([TaskType, TaskTypeWeight, Day, Task, WeeklySchedule, Availability])
