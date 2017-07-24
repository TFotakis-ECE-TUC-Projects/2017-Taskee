from django.conf.urls import url

from . import views

app_name = 'login'

urlpatterns = [
    url(r'^$', views.LoginFormView.as_view(), name='login'),
    url(r'^register/$', views.RegisterFormView.as_view(), name='register'),
    url(r'^logout/$', views.logoutView, name='logout'),
]
