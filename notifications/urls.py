from django.urls import path
from .views import NotificationListView,MarkNotificationAsRead

app_name = 'notifications'
urlpatterns = [
    path('', NotificationListView.as_view(), name='notifications-list'),
    path('<int:notification_id>/read/', MarkNotificationAsRead.as_view(), name='mark-as-read'),
]
