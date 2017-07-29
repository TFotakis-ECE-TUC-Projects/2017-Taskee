from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, DeleteView

from .models import Task, WeeklySchedule


class IndexView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'taskmanager/index.html'
    login_url = '/login/'


class CreateTask(CreateView):
    model = Task
    fields = ['name', 'user', 'type', 'place', 'notes']


class TaskView(LoginRequiredMixin, generic.ListView):
    template_name = 'taskmanager/taskView.html'
    context_object_name = 'task_list'
    login_url = '/login/'

    def get_queryset(self):
        return Task.objects.all()


class DetailView(generic.DetailView):
    model = Task
    template_name = 'taskmanager/taskDetail.html'


class DeleteTask(DeleteView):
    model = Task
    success_url = reverse_lazy('taskmanager:taskView')  # This is where this view will redirect the user
    template_name = 'delete_confirm.html'


class CreateWeeklySchedule(CreateView):
    model = WeeklySchedule
    fields = ['user', 'task', 'instanceId', 'day', 'startingTime', 'duration', 'canMove', 'valid']


class WeeklyScheduleView(LoginRequiredMixin, generic.ListView):
    template_name = 'taskmanager/weeklyScheduleView.html'
    context_object_name = 'weeklySchedule_list'
    login_url = '/login/'

    def get_queryset(self):
        return WeeklySchedule.objects.all().order_by('day', 'startingTime')


class WeeklyScheduleDetailView(generic.DetailView):
    model = WeeklySchedule
    template_name = 'taskmanager/weeklyScheduleDetails.html'
    context_object_name = 'weeklySchedule'


class DeleteWeeklySchedule(DeleteView):
    model = WeeklySchedule
    success_url = reverse_lazy('taskmanager:weeklyScheduleView')  # This is where this view will redirect the user
    template_name = 'delete_confirm.html'
    context_object_name = "object"
