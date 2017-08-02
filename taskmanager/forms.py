from django import forms

from .models import Task, WeeklySchedule, Availability


class TaskForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs = {
            'class': 'form-control'
        }
        self.fields['type'].widget.attrs = {
            'class': 'form-control'
        }
        self.fields['place'].widget.attrs = {
            'class': 'form-control'
        }
        self.fields['notes'].widget.attrs = {
            'class': 'form-control'
        }

    class Meta:
        model = Task
        fields = ['name', 'type', 'place', 'notes']


class WeeklyScheduleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(WeeklyScheduleForm, self).__init__(*args, **kwargs)
        self.fields['task'].widget.attrs = {
            'class': 'form-control'
        }
        self.fields['instanceId'].widget.attrs = {
            'class': 'form-control'
        }
        self.fields['day'].widget.attrs = {
            'class': 'form-control'
        }
        self.fields['startingTime'].widget.attrs = {
            'class': 'form-control'
        }
        self.fields['duration'].widget.attrs = {
            'class': 'form-control'
        }
        self.fields['canMove'].widget.attrs = {
            'class': 'form-control'
        }

    class Meta:
        model = WeeklySchedule
        fields = ['task', 'instanceId', 'day', 'startingTime', 'duration', 'canMove']


class AvailabilityForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AvailabilityForm, self).__init__(*args, **kwargs)
        self.fields['task'].widget.attrs = {
            'class': 'form-control'
        }
        self.fields['instanceId'].widget.attrs = {
            'class': 'form-control'
        }
        self.fields['day'].widget.attrs = {
            'class': 'form-control'
        }
        self.fields['startingTime'].widget.attrs = {
            'class': 'form-control'
        }
        self.fields['endingTime'].widget.attrs = {
            'class': 'form-control'
        }
        self.fields['priority'].widget.attrs = {
            'class': 'form-control'
        }

    class Meta:
        model = Availability
        fields = ['task', 'instanceId', 'day', 'startingTime', 'endingTime', 'priority']
