from django.conf.urls import url

from . import views

app_name = 'taskmanager'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<primaryKey>[0-9]+)/$', views.taskdetail, name='detail'),
]
