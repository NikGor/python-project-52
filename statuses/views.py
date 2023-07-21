from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Status
from .forms import StatusForm
from django.utils.translation import gettext as _


class StatusListView(LoginRequiredMixin, ListView):
    model = Status
    template_name = 'statuses/statuses.html'
    context_object_name = 'statuses'


class StatusCreateView(LoginRequiredMixin, CreateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/status_create.html'
    success_url = reverse_lazy('statuses:status_list')

    def form_valid(self, form):
        messages.success(self.request, _('Статус успешно создан'))
        return super().form_valid(form)


class StatusUpdateView(LoginRequiredMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/status_update.html'
    success_url = reverse_lazy('statuses:status_list')

    def form_valid(self, form):
        messages.success(self.request, _('Статус успешно изменен'))
        return super().form_valid(form)


class StatusDeleteView(LoginRequiredMixin, DeleteView):
    model = Status
    template_name = 'statuses/status_delete.html'
    success_url = reverse_lazy('statuses:status_list')

    def form_valid(self, form):
        self.object = self.get_object()
        if self.object.task_set.exists():
            messages.error(self.request, _('Невозможно удалить статус, связанный с задачами.'))
            return redirect('statuses:status_list')
        self.object.__class__.objects.filter(id=self.object.id).delete()
        messages.success(self.request, _('Статус успешно удален'))
        return super().form_valid(form)