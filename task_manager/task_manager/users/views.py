from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import LoginView


class CustomUserCreationForm(UserCreationForm):
    email = None


class UserListView(ListView):
    model = User
    template_name = 'users/user_list.html'


class UserCreateView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('user_list')


class UserUpdateView(UpdateView):
    model = User
    form_class = UserChangeForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('user_list')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.add_message(request, messages.INFO, 'You must be logged in to edit a user.')
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)


class UserDeleteView(DeleteView):
    model = User
    template_name = 'users/user_confirm_delete.html'
    success_url = reverse_lazy('user_list')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.add_message(request, messages.INFO, 'You must be logged in to delete a user.')
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Вы успешно вошли в систему!")
        return response


@login_required
def profile(request):
    return render(request, 'users/profile.html')