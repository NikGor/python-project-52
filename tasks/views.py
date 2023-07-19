from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .forms import TaskForm, FilterForm
from .models import Task
from statuses.models import Status
from users.models import User
from labels.models import Label
from django.contrib import messages


@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    labels = task.labels.all()
    return render(request, 'tasks/task_detail.html', {'task': task, 'labels': labels})


@login_required
def tasks(request):
    tasks = Task.objects.all()
    statuses = Status.objects.all()
    users = User.objects.all()
    labels = Label.objects.all()

    form = FilterForm(request.GET)

    if form.is_valid():
        name_search = form.cleaned_data.get('name')
        status_filter = form.cleaned_data.get('status')
        assignee_filter = form.cleaned_data.get('assignee')
        label_filter = form.cleaned_data.get('labels')
        only_mine = form.cleaned_data.get('only_mine')

        if only_mine:
            tasks = tasks.filter(author=request.user)
        if status_filter:
            tasks = tasks.filter(status=status_filter)
        if assignee_filter:
            tasks = tasks.filter(assignee=assignee_filter)
        if name_search:
            tasks = tasks.filter(name__icontains=name_search)
        if label_filter:
            tasks = tasks.filter(labels__in=label_filter)

    return render(request, 'tasks/tasks.html', {'form': form,
                                                'tasks': tasks,
                                                'statuses': statuses,
                                                'users': users,
                                                'labels': labels})


@login_required
def task_create(request):
    statuses = Status.objects.all()
    users = User.objects.all()
    labels = Label.objects.all()
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.author = request.user
            task.save()
            form.save_m2m()
            messages.success(request, 'Задача успешно создана')
            return redirect('tasks:tasks_list')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
    else:
        form = TaskForm()
    return render(request, 'tasks/task_create.html', {'form': form,
                                                      'statuses': statuses,
                                                      'users': users,
                                                      'labels': labels})


@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    statuses = Status.objects.all()
    users = User.objects.all()
    labels = Label.objects.all()
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save(commit=False)
            task.save()
            form.save_m2m()
            messages.success(request, 'Задача успешно изменена')
            return redirect('tasks:tasks_list')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_update.html', {'form': form,
                                                      'task': task,
                                                      'statuses': statuses,
                                                      'users': users,
                                                      'labels': labels})


@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if task.author != request.user:
        messages.error(request, "Задачу может удалить только ее автор")
        return redirect('tasks:tasks_list')
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Задача успешно удалена')
        return redirect('tasks:tasks_list')
    return render(request, 'tasks/task_delete.html', {'task': task})
