from django.shortcuts import redirect
from django.views.generic import ListView,View
from .models import Notification

# Create your views here.
class MarkNotificationAsRead(View):
    def post(self, request, notification_id):
        #Get notification
        notification=Notification.objects.get(id=notification_id)
        notification.mark_as_read()
        return redirect('notifications:notifications-list')

class NotificationListView(ListView):
    model = Notification
    template_name = 'notifications/notification_list.html'
    context_object_name = 'notifications'
    paginate_by = 5

    def get_queryset(self):
        return self.request.user.notifications.unread(self.request.user)

    def get_context_data(self, **kwargs):
        #latest notifications
        context=super().get_context_data(**kwargs)
        # if self.request.user.is_authenticated:
            
        latest_notifications=self.request.user.notifications.unread(self.request.user)
        context['latest_notifications'] = latest_notifications
        context['notifications_count'] = latest_notifications.count()
        context["header_text"] = "Notifications"
        context["title"] = "All Notifications"
        return context
    