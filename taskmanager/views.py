# Create your views here.
from .models import Task
from django.views import generic
from django.http import HttpResponse

class TaskView(generic.ListView):

    template_name = 'taskView.html'
    context_object_name = 'task_list'

    def get_queryset(self):
        return Task.objects.all()

#
# class TaskDetail(generic.DetailView):
#     model = Task
#     template_name = 'taskDetail.html'
def taskdetail(request, pk):
    return HttpResponse("<h2>Details: "+str(pk))+"</h2>"