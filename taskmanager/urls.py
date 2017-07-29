from django.conf.urls import url

from . import views

app_name = 'taskmanager'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^task/(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='taskDetail'),
    url(r'^weeklySchedule/(?P<pk>[0-9]+)/$', views.WeeklyScheduleDetailView.as_view(), name='weeklyScheduleDetails'),
    url(r'addTask/$', views.CreateTask.as_view(), name='task-add'),
    url(r'addWeeklySchedule/$', views.CreateWeeklySchedule.as_view(), name='weeklySchedule-add'),
    url(r'^task/(?P<pk>\d+)/delete/$', views.DeleteTask.as_view(), name='taskDelete'),
]
