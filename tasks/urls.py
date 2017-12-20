from django.conf.urls import url
from . import views
urlpatterns = [
    # homepage
    url(r'^$', views.index, name='index'),
    url(r'^task_list/$', views.tasks, name='task_list'),
    url(r'^edit_task/(?P<task_id>\d+)/$', views.edit_task, name='edit_task'),
    url(r'^task_list/(?P<task_id>\d+)/$', views.task_detail, name='task_detail'),
]
