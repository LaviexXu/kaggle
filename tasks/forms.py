from django import forms
from .models import Task, Result


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['task_name', 'display', 'description', 'data_zip']
        widgets = {'text': forms.Textarea(attrs={'cols': 160})}


class ResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = ['result_excel', 'description']
        widgets = {'text': forms.Textarea(attrs={'cols': 160})}
