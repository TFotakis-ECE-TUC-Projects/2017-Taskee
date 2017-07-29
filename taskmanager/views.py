from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.views.generic.edit import CreateView,DeleteView
from .models import Task
from django.core.urlresolvers import reverse_lazy



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

# class DeleteTask(request):
#     model= Task
#     if request.POST.get('delete'):
#         obj.delete()

class DeleteTask(DeleteView):
    model = Task
    success_url = reverse_lazy(IndexView) # This is where this view will
                                            # redirect the user
    template_name = 'taskmanager/taskDelete.html'