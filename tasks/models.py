from django.db import models


# Create your models here.
class Task(models.Model):
    task_name = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    display = models.BooleanField(default=True)

    def _str_(self):
        return self.task_name
