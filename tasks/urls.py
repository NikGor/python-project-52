from django.urls import path
from . import views

app_name = 'tasks'

urlpatterns = [
    path('', views.tasks, name='tasks_list'),
    path('<int:pk>/', views.task_detail, name='task_detail'),
    path('create/', views.task_create, name='task_create'),
    path('<int:pk>/update/', views.task_update, name='task_update'),
    path('<int:pk>/delete/', views.task_delete, name='task_delete'),
]
