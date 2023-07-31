from django.shortcuts import render, redirect
from django.views import View
from django.views.generic.edit import FormView, DeleteView, CreateView, UpdateView
from django.urls import reverse_lazy
from task_manager.mixins import CustomLoginRequiredMixin
from .models import User
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm, UserUpdateForm
from django.utils.translation import gettext as _


class UserListView(View):
    def get(self, request):
        users = User.objects.all()
        return render(request, 'users/users.html', {'users': users})


class RegisterView(CreateView):
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


class UpdateUserView(CustomLoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'users/update_user.html'
    success_url = reverse_lazy('users:users')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.request.user == self.object:
            return super().dispatch(request, *args, **kwargs)
        else:
            messages.error(self.request, _("У вас нет прав для изменения другого пользователя."))
            return redirect('users:users')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, _("Пользователь успешно изменен"))
        update_session_auth_hash(self.request, form.instance)
        return super().form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}")
        return self.render_to_response(self.get_context_data(form=form))


class DeleteUserView(CustomLoginRequiredMixin, DeleteView):
    model = User
    template_name = 'users/delete_user.html'
    success_url = reverse_lazy('users:users')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.request.user == self.object:
            return super().dispatch(request, *args, **kwargs)
        else:
            messages.error(self.request, _("У вас нет прав для изменения другого пользователя."))
            return redirect('users:users')

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
