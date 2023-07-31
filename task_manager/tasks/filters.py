import django_filters
from task_manager.labels.models import Label
from task_manager.tasks.models import Task


class TaskFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    labels = django_filters.ModelMultipleChoiceFilter(queryset=Label.objects.all())

    class Meta:
        model = Task
        fields = ['name', 'status', 'executor', 'labels']
