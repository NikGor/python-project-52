from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import RegisterForm


def index(request):
    return render(request, 'task_manager/index.html')


def users(request):
    users = User.objects.all()
    return render(request, 'task_manager/users.html', {'users': users})


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users')
    else:
        form = RegisterForm()
    return render(request, 'task_manager/register.html', {'form': form})
