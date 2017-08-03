from django.conf.urls import url

from . import views

app_name = 'taskmanager'

urlpatterns = [
	url(r'^$', views.IndexView.as_view(), name='index'),
	url(r'^task/$', views.TaskView.as_view(), name='taskView'),
	url(r'addTask/$', views.CreateTask.as_view(), name='taskAdd'),
	url(r'^task/(?P<pk>\d+)/delete/$', views.DeleteTask.as_view(), name='taskDelete'),
	url(r'^weeklySchedule/$', views.WeeklyScheduleView.as_view(), name='weeklyScheduleView'),
	url(r'addWeeklySchedule/$', views.CreateWeeklySchedule.as_view(), name='weeklyScheduleAdd'),
	url(r'^weeklySchedule/(?P<pk>\d+)/delete/$', views.DeleteWeeklySchedule.as_view(), name='weeklyScheduleDelete'),
	url(r'^availabilities/$', views.AvailabilitiesView.as_view(), name='availabilityView'),
	url(r'^addavailabilities/$', views.CreateAvailability.as_view(), name='availabilityAdd'),
	url(r'^availabilities/(?P<pk>[0-9]+)/delete$', views.DeleteAvailabilities.as_view(), name='availabilityDelete'),
	url(r'^taskType/$', views.taskTypeView, name='taskTypeView'),
	url(r'^taskType/update$', views.taskTypeWeightUpdate, name='taskTypeUpdate'),
	url(r'^calculate', views.calculate, name='calculate'),
]
