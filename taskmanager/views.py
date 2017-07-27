from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.views.generic.edit import CreateView
from .models import Task


# generic.TemplateView
class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'taskmanager/taskView.html'
    context_object_name = 'task_list'
    login_url = '/login/'

    def get_queryset(self):
        return Task.objects.all()




class DetailView(generic.DetailView):
    model= Task
    template_name = 'taskmanager/taskDetail.html'


class CreateTask(CreateView):
    model = Task
    fields = ['name', 'user', 'type', 'place', 'notes']

