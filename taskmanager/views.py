from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect, render
from django.views import generic
from django.views.generic.edit import CreateView, DeleteView

from .forms import TaskForm, WeeklyScheduleForm, AvailabilityForm
from .models import Task, WeeklySchedule, TaskTypeWeight, Availability, Day

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
			transicion1 = False
			transicion2 = False
			ws_list = WeeklySchedule.objects.filter(user=request.user)
			critical_day = weeklySchedule.day
			critical_startime = weeklySchedule.startingTime
			critical_endingtime = weeklySchedule.endingTime
			if critical_endingtime < critical_startime:  # exoume transicion hmeras (Monday -> Tuesday)
				critical_end_day = Day.objects.get(id=weeklySchedule.day_id + 1)
				transicion1 = True
			else:
				critical_end_day = critical_day
			for ws in ws_list:  # tha kanei redirect eite sto view me air message success eite .delete(self,elpizontas)
				if not weeklySchedule.canMove:  # Todo na to doume me to availability
					if ws.endingTime < ws.startingTime:  # exoume transicion hmeras (Monday -> Tuesday)
						ws_end_day = Day.objects.get(id=ws.day_id + 1)
						transicion2 = True
					else:
						transicion2 = False
						ws_end_day = ws.day
					sameDay = ws.day == critical_day
					almost_sameDay1 = critical_end_day == ws.day
					almost_sameDay2 = ws_end_day == critical_day

					check_days = sameDay | almost_sameDay1 | almost_sameDay2

					if transicion1 & transicion2:
						return render(request=request, template_name='taskmanager/weeklyschedule_form.html',
						              context={'errorMessage': 'The schedule you are trying to create conflicts with: ' + str(ws)})
					if transicion1 & (not ((critical_startime >= ws.endingTime) & (critical_endingtime <= ws.startingTime))):
						secondHalfTaken = (critical_startime < ws.endingTime) | (critical_endingtime > ws.startingTime)  # & (critical_endingtime <= ws.startingTime)
					else:
						secondHalfTaken = (critical_startime <= ws.startingTime) & (critical_endingtime > ws.startingTime) & (critical_endingtime <= ws.startingTime)  # ([)]

					if transicion2 & (not ((critical_startime >= ws.endingTime) & (critical_endingtime <= ws.startingTime))):
						firstHalfTaken = (critical_startime < ws.endingTime) | (critical_endingtime > ws.startingTime)  # & (ws.endingTime <= critical_endingtime)
					else:
						firstHalfTaken = (ws.startingTime <= critical_startime) & (critical_startime < ws.endingTime) & (ws.endingTime <= critical_endingtime)  # [(])

					if check_days & (secondHalfTaken | firstHalfTaken):  # wholeTaken |  | partlyTaken
						return render(request=request,
						              template_name='taskmanager/weeklyschedule_form.html',
						              context={'errorMessage': 'The schedule you are trying to create conflicts with: ' + str(ws)})
			weeklySchedule.save()
			return redirect('taskmanager:weeklyScheduleView')  # Todo na baloume success message
		return render(request=request, template_name='taskmanager/weeklyschedule_form.html',
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
