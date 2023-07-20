from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Label
from .forms import LabelForm, FilterForm
from django.utils.translation import gettext as _


@login_required
def label_list(request):
    labels = Label.objects.all()
    form = FilterForm(request.GET)
    if form.is_valid():
        name_search = form.cleaned_data.get('name')
        not_used = form.cleaned_data.get('not_used')
        if name_search:
            labels = labels.filter(name__icontains=name_search)
        if not_used:
            labels = labels.filter(tasks=None)
    return render(request, 'labels/labels.html', {'labels': labels})


@login_required
def label_create(request):
    if request.method == 'POST':
        form = LabelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('Метка успешно создана'))
            return redirect('labels:label_list')
    else:
        form = LabelForm()
    return render(request, 'labels/label_create.html', {'form': form})


@login_required
def label_update(request, pk):
    label = get_object_or_404(Label, pk=pk)
    if request.method == 'POST':
        form = LabelForm(request.POST, instance=label)
        if form.is_valid():
            form.save()
            messages.success(request, _('Метка успешно изменена'))
            return redirect('labels:label_list')
    else:
        form = LabelForm(instance=label)
    return render(request, 'labels/label_update.html', {'form': form, 'label': label})


@login_required
def label_delete(request, pk):
    label = get_object_or_404(Label, pk=pk)
    if request.method == 'POST':
        if label.tasks.exists():
            messages.error(request, _('Невозможно удалить метку, связанную с задачами.'))
            return redirect('labels:label_list')
        label.delete()
        messages.success(request, _('Метка успешно удалена'))
        return redirect('labels:label_list')
    return render(request, 'labels/label_delete.html', {'label': label})
