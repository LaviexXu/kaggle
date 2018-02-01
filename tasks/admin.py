from django.contrib import admin
from .models import Task, Result, Report

# Register your models here.
admin.site.register(Task)
admin.site.register(Result)
admin.site.register(Report)

