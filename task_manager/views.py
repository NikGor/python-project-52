from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.utils.translation import gettext as _

def index(request):
    return render(request, 'task_manager/index.html')


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
                    messages.info(request, _("Вы залогинены"))
                    return redirect("/")
                else:
                    messages.error(request, _("Этот аккаунт отключен."))
            else:
                messages.error(request, _("Неверное имя пользователя или пароль."))
        else:
            for field in form:
                for error in field.errors:
                    messages.error(request, f"{field.label}: {error}")
    form = AuthenticationForm()
    return render(request=request, template_name="task_manager/login.html", context={"form": form})


def logout_view(request):
    logout(request)
    messages.success(request, _("Вы разлогинены"))
    return redirect('index')
