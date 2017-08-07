from datetime import datetime, date

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models


class TaskType(models.Model):
	name = models.CharField(max_length=250)

	def __str__(self): return self.name

	def get_absolute_url(self):
		return reverse('taskmanager:taskTypeView')  # , kwargs={'pk': self.pk})


class TaskTypeWeight(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	taskType = models.ForeignKey(TaskType, on_delete=models.CASCADE)
	weight = models.IntegerField(default=1)

	def get_absolute_url(self):
		return reverse('taskmanager:taskTypeView')  # , kwargs={'pk': self.pk})

	def __str__(self): return self.taskType.name


class Day(models.Model):
	name = models.CharField(max_length=9)

	def __str__(self): return self.name


class Task(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	name = models.CharField(max_length=250)
	type = models.ForeignKey(TaskTypeWeight, on_delete=models.CASCADE, default=1)
	place = models.CharField(max_length=250)
	notes = models.CharField(max_length=1000)

	def get_absolute_url(self):
		return reverse('taskmanager:taskDetail', kwargs={'pk': self.pk})

	def __str__(self): return self.name


class WeeklySchedule(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	task = models.ForeignKey(Task, on_delete=models.CASCADE, default=1)
	instanceId = models.IntegerField(default=1)
	day = models.ForeignKey(Day, on_delete=models.CASCADE, default=1)
	startingTime = models.TimeField()
	duration = models.DurationField()
	canMove = models.BooleanField(default=False)
	valid = models.BooleanField(default=False)
	totalWeight = models.IntegerField(default=1)

	def __str__(self): return self.task.name + ' - ' + self.day.name + ' ' + str(self.startingTime)

	def get_absolute_url(self):
		return reverse('taskmanager:weeklyScheduleDetail', kwargs={'pk': self.pk})

	@property
	def endingTime(self):
		return (datetime.combine(date.today(), self.startingTime) + self.duration).time()


class Availability(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	task = models.ForeignKey(Task, on_delete=models.CASCADE, default=1)
	instanceId = models.IntegerField(default=1)
	day = models.ForeignKey(Day, on_delete=models.CASCADE, default=1)
	startingTime = models.TimeField()
	endingAvailableTime = models.TimeField()
	priority = models.IntegerField(default=1)
	used = models.BooleanField(default=False)
	totalWeight = models.IntegerField(default=1)

	def __str__(self): return self.task.name + ' - ' + self.day.name

	def get_absolute_url(self):
		return reverse('taskmanager:availabilityDetails', kwargs={'pk': self.pk})

	@property
	def endingTime(self):
		return (datetime.combine(date.today(), self.startingTime) + WeeklySchedule.objects.filter(user=self.user, task=self.task, instanceId=self.instanceId).get().duration).time()
