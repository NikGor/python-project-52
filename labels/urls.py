from django.urls import path
from . import views

app_name = 'labels'
urlpatterns = [
    path('', views.label_list, name='label_list'),
    path('create/', views.label_create, name='label_create'),
    path('<int:pk>/update/', views.label_update, name='label_update'),
    path('<int:pk>/delete/', views.label_delete, name='label_delete'),
]
