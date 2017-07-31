from .models import TaskType, TaskTypeWeight


# noinspection PyUnusedLocal
def init_new_user(instance, created, raw, **kwargs):
    if created and not raw:
        for taskType in TaskType.objects.all():
            TaskTypeWeight.objects.create(user=instance, taskType=taskType, weight=taskType.pk)
