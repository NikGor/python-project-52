from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic.edit import FormView, DeleteView
from django.urls import reverse_lazy
from .models import User
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm
from django.utils.translation import gettext as _


class UserListView(View):
    def get(self, request):
        users = User.objects.all()
        return render(request, 'users/users.html', {'users': users})


class RegisterView(FormView):
    form_class = RegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, _("Пользователь успешно зарегистрирован"))
        return super().form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}")
        return super().form_invalid(form)


class UpdateUserView(LoginRequiredMixin, FormView):
    form_class = RegisterForm
    template_name = 'users/update_user.html'
    success_url = reverse_lazy('users:users')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'instance': get_object_or_404(User, pk=self.kwargs['pk'])})
        return kwargs

    def form_valid(self, form):
        form.save()
        messages.success(self.request, _("Пользователь успешно изменен"))
        update_session_auth_hash(self.request, form.instance)
        return super().form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}")
        return super().form_invalid(form)


class DeleteUserView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'users/delete_user.html'
    success_url = reverse_lazy('users:users')

    def form_valid(self, form):
        messages.success(self.request, _("Пользователь успешно удален"))
        return super().form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}")
        return super().form_invalid(form)


class LoginView(FormView):
    form_class = AuthenticationForm
    template_name = 'users/login.html'
    success_url = reverse_lazy('/')

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(self.request, user)
                messages.info(self.request, _("Вы залогинены"))
            else:
                messages.error(self.request, _("Этот аккаунт отключен."))
        else:
            messages.error(self.request, _("Неверное имя пользователя или пароль."))
        return super().form_valid(form)


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, _("Вы разлогинены"))
        return redirect('login')
