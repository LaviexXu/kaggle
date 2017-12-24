from django.db import models


def task_file_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'task_{0}/{1}'.format(instance.id, filename)


# Create your models here.
class Task(models.Model):
    task_name = models.CharField(max_length=200)
    description = models.TextField(null=True)
    data_zip = models.FileField(upload_to=task_file_directory_path, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    display = models.BooleanField(default=True)

    def _str_(self):
        return self.task_name

    def _unicode_(self):
        return self.task_name
