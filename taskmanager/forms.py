from django import forms

from .models import Task, WeeklySchedule, Availability


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'type', 'place', 'notes']


class WeeklyScheduleForm(forms.ModelForm):
    class Meta:
        model = WeeklySchedule
        fields = ['task', 'instanceId', 'day', 'startingTime', 'duration', 'canMove']


class AvailabilityForm(forms.ModelForm):
    class Meta:
        model = Availability
        fields = ['task', 'instanceId', 'day', 'startingTime', 'endingTime', 'priority']
