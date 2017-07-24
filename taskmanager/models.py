from django.db import models


# Create your models here.
class Task:
    name = models.CharField(max_length=250)
    type = models.CharField(max_length=250)
    # ------------------------------------------------------
    startTimes = models.TimeField()[10]
    endTimes = models.TimeField()[10]
    allDay = models.BooleanField(default=False)
    # people = models.CharField(max_length=250)[10]
    places = models.CharField(max_length=250)[10]
    color = models.CharField(max_length=6)
    notes = models.CharField(max_length=1000)
    isRepetitive = models.IntegerField(default=1)
    # class Repetitiveness(Enum):
    #     NEVER = 1
    #     DAILY = 2
    #     WEEKLY = 3
    #     MONTHLY = 4
    #     YEARLY = 5
    everyNumOfDays = models.IntegerField(default=0)
    everyNumOfWeeks = models.IntegerField(default=0)
    availableWeekDays = models.BooleanField(default=False)
    everyNumOfMonths = models.IntegerField(default=0)
    monthlyRepetition = models.BooleanField()
    # class MonthlyRepetition(Enum):
    #     # on the 20th of each month
    #     SAME_DATE_EACH_MONTH = 1
    #     # on the third Thursday each month
    #     SAME_DAY_EACH_MONTH = 2
    everyNumOfYears = models.IntegerField(default=0)
    repetitionEndDate = models.DateField()

    priority = models.IntegerField()
    obligatory = models.BooleanField()
    availableStartTimes = models.TimeField()
    availableEndTimes = models.TimeField()
    availableStartDates = models.DateField()
    availableEndDates = models.DateField()


class AvailableWeekDays:
    task = Task()
    Monday = models.BooleanField(default=False)
    Tuesday = models.BooleanField(default=False)
    Wednesday = models.BooleanField(default=False)
    Thursday = models.BooleanField(default=False)
    Friday = models.BooleanField(default=False)
    Saturday = models.BooleanField(default=False)
    Sunday = models.BooleanField(default=False)
