from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Task(models.Model):
    task_name = models.CharField(max_length=200)
    description = models.TextField(null=True)
    data_zip = models.FileField(upload_to='task_data', null=True)
    result_csv = models.FileField(upload_to='task_data', null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    display = models.BooleanField(default=True)

    def _str_(self):
        return self.task_name

    def _unicode_(self):
        return self.task_name


def _upload_path(instance, filename):
    return instance.get_upload_path(filename)


class Result(models.Model):
    task = models.ForeignKey(Task)
    user = models.ForeignKey(User)
    result_csv = models.FileField(upload_to=_upload_path)
    description = models.TextField(null=True)
    date_added = models.DateTimeField(auto_now_add=True,null=True)
    score = models.DecimalField(max_digits=7, decimal_places=5, default=10)

    def get_upload_path(self, filename):
        return str(self.user.username) + "/" + 'task_' + str(self.task.id) + "/" + filename


class Report(models.Model):
    task = models.ForeignKey(Task)
    user = models.ForeignKey(User)
    report = models.FileField(upload_to=_upload_path)

    def get_upload_path(self, filename):
        return str(self.user.username) + "/" + 'task_' + str(self.task.id) + "/" + filename
