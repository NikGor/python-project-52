from django.urls import path
from . import views

app_name = 'statuses'

urlpatterns = [
    path('', views.status_list, name='status_list'),
    path('create/', views.status_create, name='status_create'),
    path('<int:pk>/update/', views.status_update, name='status_update'),
    path('<int:pk>/delete/', views.status_delete, name='status_delete'),
]
