from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect, render
from django.views import generic
from django.views.generic.edit import CreateView, DeleteView

from .calculator import hasConflict, arrangeTasks
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
		return redirect('taskmanager:taskAdd')


class TaskView(LoginRequiredMixin, generic.ListView):
	template_name = 'taskmanager/taskView.html'
	context_object_name = 'task_list'
	login_url = LOGIN_URL

	def get_queryset(self):
		# return Task.objects.all()
		return Task.objects.filter(user=self.request.user)


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
			critical = form.save(commit=False)
			critical.user = request.user
			critical.task = form.cleaned_data['task']
			critical.instanceId = form.cleaned_data['instanceId']
			critical.day = form.cleaned_data['day']
			critical.startingTime = form.cleaned_data['startingTime']
			critical.duration = form.cleaned_data['duration']
			critical.canMove = form.cleaned_data['canMove']
			critical.valid = not critical.canMove
			ws_list = WeeklySchedule.objects.filter(user=request.user)
			for ws in ws_list:  # tha kanei redirect eite sto view me air message success eite .delete(self,elpizontas)
				if hasConflict(critical, ws):
					if critical.canMove:
						critical.save()
						return redirect('taskmanager:weeklyScheduleView')
					else:
						return render(request=request, template_name='errorView.html',
						              context={'errorMessage': 'The schedule you are trying to create conflicts with: ' + str(ws)})
			critical.valid = True
			critical.save()
			return redirect('taskmanager:weeklyScheduleView')  # Todo na baloume success message
		return render(request=request, template_name='errorView.html',
		              context={'errorMessage': 'The form is not valid'})


class WeeklyScheduleView(LoginRequiredMixin, generic.ListView):
	template_name = 'taskmanager/weeklyScheduleView.html'
	context_object_name = 'weeklySchedule_list'
	login_url = LOGIN_URL

	def get_queryset(self):
		return WeeklySchedule.objects.filter(user=self.request.user).order_by('day', 'startingTime')


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
			availability.endingAvailableTime = form.cleaned_data['endingAvailableTime']
			availability.priority = form.cleaned_data['priority']
			availability.totalWeight = availability.priority * availability.task.type.weight
			availability.save()
			return redirect('taskmanager:availabilityView')
		return redirect('taskmanager:availabilityAdd')


class AvailabilitiesView(LoginRequiredMixin, generic.ListView):
	template_name = 'taskmanager/availabilitiesView.html'
	context_object_name = 'availability_list'
	login_url = LOGIN_URL

	def get_queryset(self):
		return Availability.objects.filter(user=self.request.user).order_by('day', 'startingTime')


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


def taskTypeWeightUpdate(request):
	taskTypeWeightList = TaskTypeWeight.objects.filter(user=request.user)
	for taskTypeWeight in taskTypeWeightList:
		try:
			weight = request.POST[str(taskTypeWeight.id)]
		except:
			return render(request, 'errorView.html',
			              {"errorMessage": "An error occured. Please try again"})
		else:
			tmpTask = TaskTypeWeight.objects.filter(pk=taskTypeWeight.id).get()
			tmpTask.weight = int(weight)
			tmpTask.save()
			taskList = Task.objects.filter(user=request.user, type=taskTypeWeight.id)
			for task in taskList:
				availabilityList = Availability.objects.filter(user=request.user, task=task)
				for availability in availabilityList:
					availability.totalWeight = availability.priority * tmpTask.weight
					availability.save()
	return redirect('taskmanager:taskTypeView')


def calculate(request):
	if arrangeTasks(request.user):
		return render(request=request, template_name='taskmanager/index.html', context={'message': 'Successfully Calculated', 'textClass': 'text-success'})
	else:
		return render(request=request, template_name='taskmanager/index.html', context={'message': 'Something went wrong... Please try again', 'textClass': 'text-danger'})
