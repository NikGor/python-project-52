from django import forms
from .models import Task
from task_manager.statuses.models import Status
from task_manager.users.models import User
from task_manager.labels.models import Label


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'labels']


class FilterForm(forms.Form):
    name = forms.CharField(max_length=100,
                           required=False,
                           widget=forms.TextInput(attrs={'placeholder': 'Имя задачи'}))
    status = forms.ModelChoiceField(queryset=Status.objects.all(),
                                    required=False,
                                    empty_label="---------")
    executor = forms.ModelChoiceField(queryset=User.objects.all(),
                                      required=False,
                                      empty_label="---------")
    label = forms.ModelChoiceField(queryset=Label.objects.all(),
                                   required=False, empty_label="Метка")
    only_mine = forms.BooleanField(required=False,
                                   label="Только мои")
