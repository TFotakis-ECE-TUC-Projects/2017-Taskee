from django.conf.urls import url

from . import views

app_name = 'taskmanager'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),

    url(r'^task/$', views.TaskView.as_view(), name='taskView'),
    url(r'^task/(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='taskDetail'),
    url(r'addTask/$', views.CreateTask.as_view(), name='task-add'),
    url(r'^task/(?P<pk>\d+)/delete/$', views.DeleteTask.as_view(), name='taskDelete'),

    url(r'^weeklySchedule/(?P<pk>[0-9]+)/$', views.WeeklyScheduleDetailView.as_view(), name='weeklyScheduleDetails'),
    url(r'^weeklySchedule/$', views.WeeklyScheduleView.as_view(), name='weeklyScheduleView'),
    url(r'addWeeklySchedule/$', views.CreateWeeklySchedule.as_view(), name='weeklySchedule-add'),
    url(r'^weeklySchedule/(?P<pk>\d+)/delete/$', views.DeleteWeeklySchedule.as_view(), name='weeklyScheduleDelete'),

    url(r'^availabilities/$', views.AvailabilitiesView.as_view(), name='availabilityView'),
    url(r'^availabilities/(?P<pk>[0-9]+)/$', views.AvailabilitiesDetailView.as_view(), name='availabilityDetails'),
    url(r'^addavailabilities/$', views.CreateAvailability.as_view(), name='availability-add'),
    url(r'^availabilities/(?P<pk>[0-9]+)/delete$', views.DeleteAvailabilities.as_view(), name='availabilityDelete'),

    url(r'addTaskType/$', views.CreateTaskType.as_view(), name='taskType-add'),
    url(r'^taskType/$', views.TaskTypeView.as_view(), name='taskTypeView'),
    url(r'^taskType/(?P<pk>[0-9]+)/$', views.TaskTypeDetailView.as_view(), name='taskTypeDetail'),
    url(r'^taskType/(?P<pk>\d+)/delete/$', views.DeleteTaskType.as_view(), name='taskTypeDelete'),

    url(r'addTaskTypeWeight/$', views.CreateTaskTypeWeight.as_view(), name='taskTypeWeight-add'),
    url(r'^taskTypeWeight/$', views.TaskTypeWeightView.as_view(), name='taskTypeWeightUpdate'),
]
