from django.conf.urls import url

from . import views

app_name = 'taskmanager'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'add/$', views.CreateTask.as_view(), name='task-add'),
    url(r'^(?P<pk>\d+)/delete/$', views.DeleteTask.as_view(), name='delete'),
]
