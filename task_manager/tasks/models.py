from django.db import models
from django.conf import settings
from task_manager.labels.models import Label


class Task(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    status = models.ForeignKey('statuses.Status', on_delete=models.CASCADE)
    labels = models.ManyToManyField(Label, related_name='tasks', blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name='author_tasks')
    executor = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 related_name='assigned_tasks',
                                 blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
