from django.contrib.auth.models import User
from django.db import models


class TaskType(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self): return self.name


class TaskTypeWeight(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    taskType = models.ForeignKey(TaskType, on_delete=models.CASCADE)
    weight = models.IntegerField(default=1)

    def __str__(self): return self.taskType.name


class Day(models.Model):
    name = models.CharField(max_length=9)

    def __str__(self): return self.name


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    type = models.ForeignKey(TaskType, on_delete=models.CASCADE, default=1)
    place = models.CharField(max_length=250)
    notes = models.CharField(max_length=1000)

    def __str__(self): return self.name


class WeeklySchedule(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, default=1)
    instanceId = models.IntegerField(default=1)
    day = models.ForeignKey(Day, on_delete=models.CASCADE, default=1)
    startingTime = models.TimeField()
    duration = models.TimeField()
    canMove = models.BooleanField(default=False)
    valid = models.BooleanField(default=False)

    def __str__(self): return self.task.name + ' - ' + self.day.name + ' ' + str(self.startingTime)


class Availability(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, default=1)
    instanceId = models.IntegerField(default=1)
    day = models.ForeignKey(Day, on_delete=models.CASCADE, default=1)
    startingTime = models.TimeField()
    endingTime = models.TimeField()
    priority = models.IntegerField(default=1)

    def __str__(self): return self.task.name + ' - ' + self.day.name
