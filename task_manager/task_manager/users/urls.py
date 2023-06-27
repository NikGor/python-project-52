from django.urls import path
from .views import UserListView, UserCreateView, UserUpdateView, UserDeleteView, CustomLoginView
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('', UserListView.as_view(), name='user_list'),
    path('create/', UserCreateView.as_view(), name='user_create'),
    path('<int:pk>/update/', UserUpdateView.as_view(), name='user_update'),
    path('<int:pk>/delete/', UserDeleteView.as_view(), name='user_delete'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
