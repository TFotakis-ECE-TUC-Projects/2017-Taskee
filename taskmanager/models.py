from django.db import models


class TaskType(models.Model):
    name = models.CharField(max_length=250)
    weight = models.IntegerField()

    def __str__(self):
        return self.name


class Task(models.Model):
    name = models.CharField(max_length=250)
    type = models.ForeignKey(TaskType, on_delete=models.CASCADE, default=1)
    place = models.CharField(max_length=250)
    notes = models.CharField(max_length=1000)

    def __str__(self):
        return self.name


class WeeklySchedule(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, default=1)
    instanceId = models.IntegerField(default=0)
    day = models.CharField(max_length=9)
    startingTime = models.TimeField()
    duration = models.TimeField()
    canMove = models.BooleanField(default=False)
    valid = models.BooleanField(default=False)


class Availability(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, default=1)
    instanceId = models.IntegerField()
    day = models.CharField(max_length=9)
    startingTime = models.TimeField()
    endingTime = models.TimeField()
    priority = models.IntegerField()
