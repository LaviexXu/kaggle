from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    # homepage
    url(r'^$', views.index, name='index'),
    url(r'^task_list/$', views.tasks, name='task_list'),
    url(r'^edit_task/(?P<task_id>\d+)/$', views.edit_task, name='edit_task'),
    url(r'^task_list/(?P<task_id>\d+)/$', views.task_detail, name='task_detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
