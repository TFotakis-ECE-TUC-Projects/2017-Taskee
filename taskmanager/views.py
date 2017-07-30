from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.views import generic
from django.views.generic.edit import CreateView, DeleteView

from .models import Task, WeeklySchedule, Availability, TaskType
from .forms import TaskForm, WeeklyScheduleForm, AvailabilityForm
from .models import Task, WeeklySchedule


class IndexView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'taskmanager/index.html'
    login_url = '/login/'


######## Task ########
class CreateTask(CreateView):
    model = Task
    form_class = TaskForm

    def post(self, request):
        form = self.form_class(data=request.POST)

        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.name = form.cleaned_data['name']
            task.type = form.cleaned_data['type']
            task.place = form.cleaned_data['place']
            task.notes = form.cleaned_data['notes']
            task.save()
            return redirect('taskmanager:taskView')
        return redirect('taskmanager:task-add')


class TaskView(LoginRequiredMixin, generic.ListView):
    template_name = 'taskmanager/taskView.html'
    context_object_name = 'task_list'
    login_url = '/login/'

    def get_queryset(self):
        # return Task.objects.all()
        return Task.objects.filter(user=self.request.user)


class DetailView(generic.DetailView):
    model = Task
    template_name = 'taskmanager/taskDetail.html'


class DeleteTask(DeleteView):
    model = Task
    success_url = reverse_lazy('taskmanager:taskView')  # This is where this view will redirect the user
    template_name = 'delete_confirm.html'

######### WeeklySchedule ###########

class CreateWeeklySchedule(CreateView):
    model = WeeklySchedule
    form_class = WeeklyScheduleForm

    def post(self, request):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            weeklySchedule = form.save(commit=False)
            weeklySchedule.user = request.user
            weeklySchedule.task = form.cleaned_data['task']
            weeklySchedule.instanceId = form.cleaned_data['instanceId']
            weeklySchedule.day = form.cleaned_data['day']
            weeklySchedule.startingTime = form.cleaned_data['startingTime']
            weeklySchedule.duration = form.cleaned_data['duration']
            weeklySchedule.canMove = form.cleaned_data['canMove']
            weeklySchedule.valid = form.cleaned_data['valid']
            weeklySchedule.save()
            return redirect('taskmanager:weeklyScheduleView')
        return redirect('taskmanager:weeklySchedule-add')


class WeeklyScheduleView(LoginRequiredMixin, generic.ListView):
    template_name = 'taskmanager/weeklyScheduleView.html'
    context_object_name = 'weeklySchedule_list'
    login_url = '/login/'

    def get_queryset(self):
        # return WeeklySchedule.objects.all().order_by('day', 'startingTime')
        return WeeklySchedule.objects.filter(user=self.request.user).order_by('day', 'startingTime')


class WeeklyScheduleDetailView(generic.DetailView):
    model = WeeklySchedule
    template_name = 'taskmanager/weeklyScheduleDetails.html'
    context_object_name = 'weeklySchedule'


class DeleteWeeklySchedule(DeleteView):
    model = WeeklySchedule
    success_url = reverse_lazy('taskmanager:weeklyScheduleView')  # This is where this view will redirect the user
    template_name = 'delete_confirm.html'
    context_object_name = "object"



########## Availability ###################

class CreateAvailability(CreateView):
    model = Availability
    form_class = AvailabilityForm

    def post(self, request):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            availability = form.save(commit=False)
            availability.user = request.user
            availability.task = form.cleaned_data['task']
            availability.instanceId = form.cleaned_data['instanceId']
            availability.day = form.cleaned_data['day']
            availability.startingTime = form.cleaned_data['startingTime']
            availability.endingTime = form.cleaned_data['duration']
            availability.priority = form.cleaned_data['priority']
            availability.save()
            return redirect('taskmanager:availabilityView')
        return redirect('taskmanager:availability-add')

class AvailabilitiesView(LoginRequiredMixin, generic.ListView):
    template_name = 'taskmanager/availabilitiesView.html'
    context_object_name = 'availability_list'
    login_url = '/login/'

    def get_queryset(self):
        return Availability.objects.filter(user=self.request.user).order_by('day', 'startingTime')

class AvailabilitiesDetailView(generic.DetailView):
    model = Availability
    template_name = 'taskmanager/availabilitiesDetails.html'
    context_object_name = "availability"

class DeleteAvailabilities(DeleteView):
    model = Availability
    success_url = reverse_lazy('taskmanager:availabilityView')  # This is where this view will redirect the user
    template_name = 'delete_confirm.html'
    context_object_name = "object"
###########################################


######### Tasktype ########

class CreateTaskType(CreateView):
    model = TaskType
    fields = ['name']



class TaskTypeView(LoginRequiredMixin, generic.ListView):
    model = TaskType
    template_name = 'taskmanager/taskTypeView.html'
    context_object_name = 'taskType_list'
    login_url = '/login/'

    # def get_queryset(self):
    #      #return TaskType.objects.all()
    #      return Task.objects.filter(user=self.request.user)


class DeleteTaskType(DeleteView):
    model = TaskType
    success_url = reverse_lazy('taskmanager:taskTypeView')  # This is where this view will redirect the user
    template_name = 'delete_confirm.html'
    context_object_name = "object"



class TaskTypeDetailView(generic.DetailView):
    model = TaskType
    template_name = 'taskmanager/taskTypeDetails.html'
    context_object_name = 'taskType'