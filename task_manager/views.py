from django.contrib.auth.views import LoginView as AuthLoginView, LogoutView as AuthLogoutView
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.utils.translation import gettext as _


class IndexView(TemplateView):
    template_name = 'task_manager/index.html'


class LoginView(AuthLoginView):
    template_name = 'task_manager/login.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        messages.info(self.request, _("Вы залогинены"))
        return super().form_valid(form)

    def form_invalid(self, form):
        for field in form:
            for error in field.errors:
                messages.error(self.request, f"{field.label}: {error}")
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('index')


class LogoutView(AuthLogoutView):
    next_page = 'index'

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, _("Вы разлогинены"))
        return super().dispatch(request, *args, **kwargs)
