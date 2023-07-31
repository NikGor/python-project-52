from django.urls import path
from . import views

app_name = 'statuses'

urlpatterns = [
    path('', views.StatusListView.as_view(), name='status_list'),
    path('create/', views.StatusCreateView.as_view(), name='status_create'),
    path('<int:pk>/update/', views.StatusUpdateView.as_view(), name='status_update'),
    path('<int:pk>/delete/', views.StatusDeleteView.as_view(), name='status_delete'),
]
