from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "password1", "password2"]


class UserUpdateForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
