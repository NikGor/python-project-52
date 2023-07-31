from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy


class CustomLoginRequiredMixin(LoginRequiredMixin):
    """Require that the user is authenticated."""

    def handle_no_permission(self):
        messages.error(self.request, "Вы не авторизованы! Пожалуйста, выполните вход.")
        return redirect(reverse_lazy('login'))
