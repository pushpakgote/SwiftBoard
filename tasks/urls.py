from django.urls import path
from .views import update_task_status_ajax,create_task_ajax

app_name = 'tasks'

urlpatterns = [
    path('update-task-status-ajax/<uuid:task_id>/', update_task_status_ajax, name='update-task-status-ajax'),
    path('create-task-ajax/', create_task_ajax, name='create-task-ajax'),
]