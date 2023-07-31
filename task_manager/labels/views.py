from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from task_manager.mixins import CustomLoginRequiredMixin
from .models import Label
from .forms import LabelForm, FilterForm
from django.utils.translation import gettext as _


class LabelListView(CustomLoginRequiredMixin, ListView):
    model = Label
    template_name = 'labels/labels.html'
    context_object_name = 'labels'

    def get_queryset(self):
        labels = super().get_queryset()
        form = FilterForm(self.request.GET)
        if form.is_valid():
            name_search = form.cleaned_data.get('name')
            not_used = form.cleaned_data.get('not_used')
            if name_search:
                labels = labels.filter(name__icontains=name_search)
            if not_used:
                labels = labels.filter(tasks=None)
        return labels


class LabelCreateView(CustomLoginRequiredMixin, CreateView):
    model = Label
    form_class = LabelForm
    template_name = 'labels/label_create.html'
    success_url = reverse_lazy('labels:label_list')

    def form_valid(self, form):
        messages.success(self.request, _('Метка успешно создана'))
        return super().form_valid(form)


class LabelUpdateView(CustomLoginRequiredMixin, UpdateView):
    model = Label
    form_class = LabelForm
    template_name = 'labels/label_update.html'
    success_url = reverse_lazy('labels:label_list')

    def form_valid(self, form):
        messages.success(self.request, _('Метка успешно изменена'))
        return super().form_valid(form)


class LabelDeleteView(CustomLoginRequiredMixin, DeleteView):
    model = Label
    template_name = 'labels/label_delete.html'
    success_url = reverse_lazy('labels:label_list')

    def form_valid(self, form):
        self.object = self.get_object()
        if self.object.tasks.exists():
            messages.error(self.request, _('Невозможно удалить метку, связанную с задачами.'))
            return redirect('labels:label_list')
        messages.success(self.request, _('Метка успешно удалена'))
        return super().form_valid(form)
