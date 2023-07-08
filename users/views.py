from django.shortcuts import render, redirect, get_object_or_404
from .models import User
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm


# Create your views here.
def users(request):
    users = User.objects.all()
    return render(request, 'users/users.html', {'users': users})


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Пользователь успешно зарегистрирован")
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
                    print(form.errors)
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})


def update_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    if not request.user.is_authenticated:
        messages.error(request, "Вы не авторизованы! Пожалуйста, выполните вход.")
        return redirect('login')
    if request.user != user:
        messages.error(request, "У вас нет прав для изменения другого пользователя.")
        return redirect('users:users')
    if request.method == "POST":
        form = RegisterForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Пользователь успешно изменен")
            update_session_auth_hash(request, user)
            return redirect('users:users')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
    else:
        form = RegisterForm(instance=user)
    return render(request, 'users/update_user.html', {'form': form})


def delete_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    if not request.user.is_authenticated:
        messages.error(request, "Вы не авторизованы! Пожалуйста, выполните вход.")
        return redirect('login')
    if request.user != user:
        messages.error(request, "У вас нет прав для изменения другого пользователя.")
        return redirect('users:users')
    if request.method == 'POST':
        user.delete()
        messages.success(request, "Пользователь успешно удален")
        return redirect('users:users')
    return render(request, 'users/delete_user.html', {'user': user})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.info(request, "Вы залогинены")
                    return redirect("/")
                else:
                    messages.error(request, "Этот аккаунт отключен.")
            else:
                messages.error(request, "Неверное имя пользователя или пароль.")
        else:
            for field in form:
                for error in field.errors:
                    messages.error(request, f"{field.label}: {error}")
    form = AuthenticationForm()
    return render(request=request, template_name="users/login.html", context={"form": form})


def logout_view(request):
    logout(request)
    messages.success(request, "Вы разлогинены")
    return redirect('login')
