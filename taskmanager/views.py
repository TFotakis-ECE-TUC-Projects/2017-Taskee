from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic

from .models import Task


# generic.TemplateView
class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'taskmanager/taskView.html'
    context_object_name = 'task_list'
    login_url = '/login/'

    def get_queryset(self):
        return Task.objects.all()


@login_required(login_url='/login/')
def taskdetail(request, primaryKey):
    task = Task.objects.filter(id=primaryKey)
    # return HttpResponse("<h2>Details: " + str(pk) + "</h2>")
    return render(request, 'taskmanager/taskDetail.html', {'task': task})
