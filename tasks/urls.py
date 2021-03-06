from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^task_list/$', views.tasks, name='task_list'),
    url(r'^edit_task/(?P<task_id>\d+)/$', views.edit_task, name='edit_task'),
    url(r'^task_list/(?P<task_id>\d+)/$', views.task_detail, name='task_detail'),
    url(r'^new_email/$', views.new_email, name='new_email'),
    url(r'^new_task/$', views.new_task, name='new_task'),
    url(r'^task_list/(?P<task_id>\d+)/description/$', views.task_description, name='task_description'),
    url(r'^task_list/(?P<task_id>\d+)/data/$', views.task_data, name='task_data'),
    url(r'^task_list/(?P<task_id>\d+)/data_download/$', views.data_download, name='data_download'),
    url(r'^task_list/(?P<task_id>\d+)/leaderboard/$', views.task_leaderboard, name='task_leaderboard'),
    url(r'^task_list/(?P<task_id>\d+)/submit_result/$', views.submit_result, name='submit_result'),
    url(r'^task_list/(?P<task_id>\d+)/my_submissions/$', views.view_submissions, name='view_submissions'),
    url(r'^task_list/(?P<task_id>\d+)/submit_report/$', views.submit_report, name='submit_report'),
    url(r'^task_list/(?P<task_id>\d+)/view_reports/$', views.view_reports, name='view_reports'),
    url(r'^task_list/(?P<task_id>\d+)/report_detail/(?P<student_id>\d+)/$',
        views.report_detail, name='report_detail'),
    url(r'^task_list/(?P<task_id>\d+)/report_download/(?P<student_id>\d+)/$',
        views.report_download, name='report_download'),
    url(r'^task_list/(?P<task_id>\d+)/report_zip_download/$',
        views.report_zip_download, name='report_zip_download')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
