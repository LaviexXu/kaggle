from django import forms
from .models import Task, Result, Report


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['task_name', 'display', 'description', 'data_zip', 'result_csv']
        widgets = {'text': forms.Textarea(attrs={'cols': 160})}


class ResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = ['result_csv', 'description']
        widgets = {'text': forms.Textarea(attrs={'cols': 160})}


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['report']
