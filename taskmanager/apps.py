from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class TaskmanagerConfig(AppConfig):
    name = 'taskmanager'
    verbose_name = _('taskmanager')

    def ready(self):
        from django.db.models.signals import post_save
        from django.contrib.auth.models import User
        from .signals import init_new_user
        post_save.connect(init_new_user, sender=User)
