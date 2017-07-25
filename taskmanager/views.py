from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views import generic

from .models import Task


# generic.TemplateView
class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'taskmanager/taskView.html'
    context_object_name = 'task_list'
    login_url = '/login/'

    def get_queryset(self):
        return Task.objects.all()


def taskdetail(request, pk):
    return HttpResponse("<h2>Details: " + str(pk) + "</h2>")
