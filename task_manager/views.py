from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.utils.translation import gettext as _
from django.views import View


class IndexView(View):
    def get(self, request):
        return render(request, 'task_manager/index.html')


class LoginView(View):
    def get(self, request):
        return render(request=request, template_name="task_manager/login.html",
                      context={"form": AuthenticationForm()})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if not form.is_valid():
            for field in form:
                for error in field.errors:
                    messages.error(request, f"{field.label}: {error}")
            return render(request=request, template_name="task_manager/login.html",
                          context={"form": form})

        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user is None:
            messages.error(request, _("Неверное имя пользователя или пароль."))
            return render(request=request, template_name="task_manager/login.html",
                          context={"form": form})

        login(request, user)
        messages.info(request, _("Вы залогинены"))
        return redirect("/")


class LogoutView(View):
    def get(self, request):
        return self.logout(request)

    def post(self, request):
        return self.logout(request)

    @staticmethod
    def logout(request):
        logout(request)
        messages.success(request, _("Вы разлогинены"))
        return redirect('index')
