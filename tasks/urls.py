from django.conf.urls import url

from . import views

app_name = 'tasks'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^show_completed_tasks/$', views.show_completed_tasks, name='show_completed_tasks'),
    url(r'^switch_(?P<display_completed_tasks>[0-1])/$', views.switch_display_completed_tasks, name='switch_display_completed_tasks'),
    url(r'^add/$', views.add, name='add'),
    url(r'^switch_finishing_(?P<task_id>[0-9]+)/$', views.switch_finishing, name='switch_finishing'),
    url(r'^edit_(?P<task_id>[0-9]+)/$', views.edit, name='edit'),
    url(r'^apply_edit_(?P<task_id>[0-9]+)/$', views.apply_edit, name='apply_edit'),
    url(r'^delete_(?P<task_id>[0-9]+)/$', views.delete, name='delete'),
]
