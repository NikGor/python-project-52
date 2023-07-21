from django.shortcuts import get_object_or_404, redirect
from django.views.generic.edit import FormView, DeleteView
from django.urls import reverse_lazy
from .forms import TaskForm, FilterForm
from .models import Task
from statuses.models import Status
from users.models import User
from labels.models import Label
from django.contrib import messages
from django.utils.translation import gettext as _
from django.views.generic import DetailView, ListView


class TaskDetailView(DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'


class TaskListView(ListView):
    model = Task
    template_name = 'tasks/tasks.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        queryset = super().get_queryset()
        form = FilterForm(self.request.GET)

        if form.is_valid():
            name_search = form.cleaned_data.get('name')
            status_filter = form.cleaned_data.get('status')
            assignee_filter = form.cleaned_data.get('assignee')
            label_filter = form.cleaned_data.get('labels')
            only_mine = form.cleaned_data.get('only_mine')

            if only_mine:
                queryset = queryset.filter(author=self.request.user)
            if status_filter is not None:
                queryset = queryset.filter(status=status_filter)
            if assignee_filter is not None:
                queryset = queryset.filter(assignee=assignee_filter)
            if name_search is not None:
                queryset = queryset.filter(name__icontains=name_search)
            if label_filter is not None:
                queryset = queryset.filter(labels__in=label_filter)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = FilterForm(self.request.GET)
        context['statuses'] = Status.objects.all()
        context['users'] = User.objects.all()
        context['labels'] = Label.objects.all()
        return context


class TaskCreateView(FormView):
    form_class = TaskForm
    template_name = 'tasks/task_create.html'
    success_url = reverse_lazy('tasks:tasks_list')

    def form_valid(self, form):
        task = form.save(commit=False)
        task.author = self.request.user
        task.save()
        form.save_m2m()
        messages.success(self.request, _('Задача успешно создана'))
        return super().form_valid(form)


class TaskUpdateView(FormView):
    form_class = TaskForm
    template_name = 'tasks/task_update.html'
    success_url = reverse_lazy('tasks:tasks_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'instance': get_object_or_404(Task, pk=self.kwargs['pk'])})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task'] = get_object_or_404(Task, pk=self.kwargs['pk'])
        context['statuses'] = Status.objects.all()
        context['labels'] = Label.objects.all()
        context['users'] = User.objects.all()
        return context

    def form_valid(self, form):
        task = form.save(commit=False)
        task.save()
        form.save_m2m()
        messages.success(self.request, _('Задача успешно изменена'))
        return super().form_valid(form)


class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'tasks/task_delete.html'
    success_url = reverse_lazy('tasks:tasks_list')

    def form_valid(self, form):
        task = self.get_object()
        if task.author != self.request.user:
            messages.error(self.request, _('Вы не можете удалить эту задачу'))
            return redirect('tasks:tasks_list')
        messages.success(self.request, _('Задача успешно удалена'))
        return super().form_valid(form)
