from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.views.generic import View

from .forms import RegisterForm
from taskmanager.models import TaskType, TaskTypeWeight

class LoginFormView(View):
    form_class = AuthenticationForm
    template_name = 'login/login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('taskmanager:index')
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(data=request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('taskmanager:index')
        return render(request, self.template_name, {'form': form})


class RegisterFormView(View):
    form_class = RegisterForm
    template_name = 'login/register.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            for taskType in TaskType.objects.all():
                TaskTypeWeight.objects.create(user=user, taskType=taskType, weight=taskType.pk)
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('taskmanager:index')
        return render(request, self.template_name, {'form': form})


def logoutView(request):
    logout(request)
    return redirect('login:login')
