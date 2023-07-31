from django import forms
from .models import Label


class LabelForm(forms.ModelForm):
    class Meta:
        model = Label
        fields = ['name']


class FilterForm(forms.Form):
    name = forms.CharField(max_length=100, required=False,
                           widget=forms.TextInput(attrs={'placeholder': 'Имя метки'}))
    not_used = forms.BooleanField(required=False, label="Не используется")
