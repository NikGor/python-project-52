from django.urls import path
from .views import LabelListView, LabelCreateView, LabelUpdateView, LabelDeleteView

app_name = 'labels'

urlpatterns = [
    path('', LabelListView.as_view(), name='label_list'),
    path('create/', LabelCreateView.as_view(), name='label_create'),
    path('update/<int:pk>/', LabelUpdateView.as_view(), name='label_update'),
    path('delete/<int:pk>/', LabelDeleteView.as_view(), name='label_delete'),
]
