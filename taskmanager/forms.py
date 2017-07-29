from django import forms

from .models import Task, WeeklySchedule


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'type', 'place', 'notes']


class WeeklyScheduleForm(forms.ModelForm):
    class Meta:
        model = WeeklySchedule
        fields = ['task', 'instanceId', 'day', 'startingTime', 'duration', 'canMove', 'valid']