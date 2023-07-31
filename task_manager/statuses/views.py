from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from task_manager.mixins import CustomLoginRequiredMixin
from .models import Status
from .forms import StatusForm
from django.utils.translation import gettext as _


class StatusListView(CustomLoginRequiredMixin, ListView):
    model = Status
    template_name = 'statuses/statuses.html'
    context_object_name = 'statuses'


class StatusCreateView(CustomLoginRequiredMixin, CreateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/status_create.html'
    success_url = reverse_lazy('statuses:status_list')

    def form_valid(self, form):
        messages.success(self.request, _('Статус успешно создан'))
        return super().form_valid(form)


class StatusUpdateView(CustomLoginRequiredMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/status_update.html'
    success_url = reverse_lazy('statuses:status_list')

    def form_valid(self, form):
        messages.success(self.request, _('Статус успешно изменен'))
        return super().form_valid(form)


class StatusDeleteView(CustomLoginRequiredMixin, DeleteView):
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
