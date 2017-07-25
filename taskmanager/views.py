from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic


class IndexView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'taskmanager/index.html'
    login_url = '/login/'