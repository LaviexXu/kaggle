from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['task_name', 'display']
        labels = {'task_name': ''}
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}
