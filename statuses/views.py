from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Status
from .forms import StatusForm
from django.utils.translation import gettext as _


@login_required
def status_list(request):
    statuses = Status.objects.all()
    return render(request, 'statuses/statuses.html', {'statuses': statuses})


@login_required
def status_create(request):
    if request.method == 'POST':
        form = StatusForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('Статус успешно создан'))
            return redirect('statuses:status_list')
    else:
        form = StatusForm()
    return render(request, 'statuses/status_create.html', {'form': form})


@login_required
def status_update(request, pk):
    status = get_object_or_404(Status, pk=pk)
    if request.method == 'POST':
        form = StatusForm(request.POST, instance=status)
        if form.is_valid():
            form.save()
            messages.success(request, _('Статус успешно изменен'))
            return redirect('statuses:status_list')
    else:
        form = StatusForm(instance=status)
    return render(request, 'statuses/status_update.html', {'form': form, 'status': status})


@login_required
def status_delete(request, pk):
    status = get_object_or_404(Status, pk=pk)
    if request.method == 'POST':
        try:
            status.delete()
            messages.success(request, _('Статус успешно удален'))
        except Exception:
            messages.error(request, _('Невозможно удалить статус, потому что он используется'))
        return redirect('statuses:status_list')
    return render(request, 'statuses/status_delete.html', {'status': status})
