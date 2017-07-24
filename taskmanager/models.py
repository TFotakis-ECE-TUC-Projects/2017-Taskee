from django.db import models


class TaskType(models.Model):
    name = models.CharField(max_length=250)
    weight = models.IntegerField()


class Task(models.Model):
    name = models.CharField(max_length=250)
    type = TaskType()
    place = models.CharField(max_length=250)
    notes = models.CharField(max_length=1000)


class WeeklySchedule(models.Model):
    task = Task()
    instanceId = models.IntegerField(default=0)
    day = models.CharField(max_length=9)
    startingTime = models.TimeField()
    duration = models.TimeField()
    canMove = models.BooleanField(default=False)
    valid = models.BooleanField(default=False)


class Availability(models.Model):
    task = Task()
    instanceId = models.IntegerField()
    day = models.CharField(max_length=9)
    startingTime = models.TimeField()
    endingTime = models.TimeField()
    priority = models.IntegerField()
