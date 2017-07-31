from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect, render
from django.views import generic
from django.views.generic.edit import CreateView, DeleteView

from .forms import TaskForm, WeeklyScheduleForm, AvailabilityForm
from .models import Task, WeeklySchedule, TaskTypeWeight, Availability

LOGIN_URL = '/login/'


class IndexView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'taskmanager/index.html'
    login_url = LOGIN_URL


######## Task ########
class CreateTask(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    login_url = LOGIN_URL

    def post(self, request, **kwargs):
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
    login_url = LOGIN_URL

    def get_queryset(self):
        # return Task.objects.all()
        return Task.objects.filter(user=self.request.user)


class DetailView(LoginRequiredMixin, generic.DetailView):
    model = Task
    template_name = 'taskmanager/taskDetail.html'
    login_url = LOGIN_URL


class DeleteTask(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('taskmanager:taskView')  # This is where this view will redirect the user
    template_name = 'delete_confirm.html'
    login_url = LOGIN_URL


######### WeeklySchedule ###########
class CreateWeeklySchedule(LoginRequiredMixin, CreateView):
    model = WeeklySchedule
    form_class = WeeklyScheduleForm
    login_url = LOGIN_URL

    def post(self, request, **kwargs):
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
            weeklySchedule.valid = not weeklySchedule.canMove
            # weeklySchedule.save()

            ws_list = WeeklySchedule.objects.all()
            critical_day = weeklySchedule.day
            critical_startime = weeklySchedule.startingTime
            critical_endingtime = weeklySchedule.endingTime

            for ws in ws_list:  # tha kanei redirect eite sto view me air message success eite .delete(self,elpizontas)
                if not weeklySchedule.canMove:  # Todo na to doume me to availability
                    sameDay = ws.day == critical_day
                    wholeTaken = (ws.startingTime <= critical_startime) & (critical_endingtime <= ws.endingTime)  # [()]
                    partlyTaken = (critical_startime <= ws.startingTime) & (
                    ws.startingTime <= critical_endingtime)  # ([])
                    secondHalfTaken = (critical_startime <= ws.startingTime) & (critical_endingtime < ws.endingTime) & (
                    critical_endingtime <= ws.startingTime)  # ([)]
                    firstHalfTaken = (ws.startingTime <= critical_startime) & (critical_startime < ws.endingTime) & (
                    ws.endingTime <= critical_endingtime)  # [(])
                    if sameDay & (wholeTaken | secondHalfTaken | firstHalfTaken | partlyTaken):
                        return render(request=request, template_name='taskmanager/weeklyschedule_form.html', context={
                            'errorMessage': 'The schedule you are trying to create conflicts with: ' + str(ws)})
                        # TODO: Comment cleanup
                        # return redirect('taskmanager:weeklyScheduleView')  # na baloume error message
                        # ws_endingtime = ws.endingTime
                        # if ((ws.day == critical_day) & (
                        #             ((ws.startingTime <= critical_startime) & (ws.endingTime > critical_startime)) | (
                        #                     (critical_startime <= ws.startingTime) & (
                        #                     critical_endingtime > ws.startingTime)))):  # an ginoun touta ola, DEN tha kaneis save!
                        #     return redirect('taskmanager:weeklyScheduleView')  # na baloume error message
            weeklySchedule.save()
            return redirect('taskmanager:weeklyScheduleView')  # Todo na baloume success message
        # return redirect('taskmanager:weeklySchedule-add')
        return render(request=request, template_name='taskmanager/weeklyScheduleView.html',
                      context={'errorMessage': 'The form is not valid'})


class WeeklyScheduleView(LoginRequiredMixin, generic.ListView):
    template_name = 'taskmanager/weeklyScheduleView.html'
    context_object_name = 'weeklySchedule_list'
    login_url = LOGIN_URL

    def get_queryset(self):
        return WeeklySchedule.objects.filter(user=self.request.user).order_by('day', 'startingTime')


class WeeklyScheduleDetailView(LoginRequiredMixin, generic.DetailView):
    model = WeeklySchedule
    template_name = 'taskmanager/weeklyScheduleDetails.html'
    context_object_name = 'weeklySchedule'
    login_url = LOGIN_URL


class DeleteWeeklySchedule(LoginRequiredMixin, DeleteView):
    model = WeeklySchedule
    success_url = reverse_lazy('taskmanager:weeklyScheduleView')  # This is where this view will redirect the user
    template_name = 'delete_confirm.html'
    context_object_name = "object"
    login_url = LOGIN_URL


########## Availability ###################
class CreateAvailability(LoginRequiredMixin, CreateView):
    model = Availability
    form_class = AvailabilityForm
    login_url = LOGIN_URL

    def post(self, request, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            availability = form.save(commit=False)
            availability.user = request.user
            availability.task = form.cleaned_data['task']
            availability.instanceId = form.cleaned_data['instanceId']
            availability.day = form.cleaned_data['day']
            availability.startingTime = form.cleaned_data['startingTime']
            availability.endingTime = form.cleaned_data['endingTime']
            availability.priority = form.cleaned_data['priority']
            availability.save()
            return redirect('taskmanager:availabilityView')
        return redirect('taskmanager:availability-add')


class AvailabilitiesView(LoginRequiredMixin, generic.ListView):
    template_name = 'taskmanager/availabilitiesView.html'
    context_object_name = 'availability_list'
    login_url = LOGIN_URL

    def get_queryset(self):
        return Availability.objects.filter(user=self.request.user).order_by('day', 'startingTime')


class AvailabilitiesDetailView(LoginRequiredMixin, generic.DetailView):
    model = Availability
    template_name = 'taskmanager/availabilitiesDetails.html'
    context_object_name = "availability"
    login_url = LOGIN_URL


class DeleteAvailabilities(LoginRequiredMixin, DeleteView):
    model = Availability
    success_url = reverse_lazy('taskmanager:availabilityView')  # This is where this view will redirect the user
    template_name = 'delete_confirm.html'
    context_object_name = "object"
    login_url = LOGIN_URL


######### Tasktype ########
def taskTypeView(request):
    tasks = TaskTypeWeight.objects.filter(user=request.user).order_by('-weight')
    template_name = 'taskmanager/taskTypeView.html'
    return render(request=request, template_name=template_name, context={'taskList': tasks})
    # context_object_name = 'taskList'
    # login_url = LOGIN_URL


def taskTypeWeightUpdate(request):
    tasks = TaskTypeWeight.objects.filter(user=request.user)
    for task in tasks:
        try:
            weight = request.POST[str(task.id)]
        except:
            return render(request, 'taskmanager/taskTypeView.html',
                          {"errorMessage": "An error occured. Please try again"})
        else:
            tmpTask = TaskTypeWeight.objects.filter(pk=task.id).get()
            tmpTask.weight = weight
            tmpTask.save()
    return redirect('taskmanager:taskTypeView')


# TODO Comments Cleanup
# class CreateTaskType(LoginRequiredMixin, CreateView):
#     model = TaskType
#     fields = ['name']
#     login_url = LOGIN_URL


# class DeleteTaskType(LoginRequiredMixin, DeleteView):
#     model = TaskType
#     success_url = reverse_lazy('taskmanager:taskTypeView')  # This is where this view will redirect the user
#     template_name = 'delete_confirm.html'
#     context_object_name = "object"


# class TaskTypeDetailView(LoginRequiredMixin, generic.DetailView):
#     model = TaskTypeWeight
#     template_name = 'taskmanager/taskTypeDetails.html'
#     context_object_name = 'taskTypeWeight'
#     login_url = LOGIN_URL


########### TaskType weight ##########
# class TaskTypeWeightUpdate(LoginRequiredMixin, UpdateView):
#     model = TaskTypeWeight
#     fields = ['user', 'taskType', 'weight']
#     login_url = LOGIN_URL


class ShowDetails(LoginRequiredMixin, generic.ListView):
    template_name = 'taskmanager/showdetails.html'
    context_object_name = 'weeklySchedule_list'
    login_url = LOGIN_URL

    def get_queryset(self):
        return WeeklySchedule.objects.filter(user=self.request.user).order_by('day', 'startingTime')
