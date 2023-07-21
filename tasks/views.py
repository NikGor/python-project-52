from django.contrib.auth.mixins import LoginRequiredMixin
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


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/tasks.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        queryset = super().get_queryset()
        form = FilterForm(self.request.GET)

        if form.is_valid():
            filters = {
                'name': lambda value: queryset.filter(name__icontains=value),
                'status': lambda value: queryset.filter(status=value),
                'executor': lambda value: queryset.filter(executor=value),
                'label': lambda value: queryset.filter(labels__in=[value]),
                'only_mine': lambda value: queryset.filter(
                    author=self.request.user) if value else queryset,
            }

            for field, filter_func in filters.items():
                value = form.cleaned_data.get(field)
                if value is not None:
                    queryset = filter_func(value)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = FilterForm(self.request.GET)
        context['statuses'] = Status.objects.all()
        context['users'] = User.objects.all()
        context['labels'] = Label.objects.all()
        return context


class TaskCreateView(LoginRequiredMixin, FormView):
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = FilterForm(self.request.GET)
        context['statuses'] = Status.objects.all()
        context['users'] = User.objects.all()
        context['labels'] = Label.objects.all()
        return context


class TaskUpdateView(LoginRequiredMixin, FormView):
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


class TaskDeleteView(LoginRequiredMixin, DeleteView):
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
