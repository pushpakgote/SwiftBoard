from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.
class NotificationManager(models.Manager):
    def unread(self,user):
        return self.filter(read=False).exclude(actor=user)
    
    def read(self,user):
        return self.filter(read=True).exclude(actor=user)

class Notification(models.Model):
    recipient=models.ForeignKey(User, on_delete=models.CASCADE,related_name='notifications')
    actor=models.ForeignKey(User, on_delete=models.CASCADE,related_name='actions')
    verb = models.CharField(max_length=255)
    content_type=models.ForeignKey(ContentType,on_delete=models.CASCADE)
    object_id=models.CharField(max_length=255)
    content_object=GenericForeignKey('content_type','object_id')
    created_at=models.DateTimeField(auto_now_add=True)
    read=models.BooleanField(default=False)

    objects=NotificationManager()

    def __str__(self):
        return f"{self.actor} {self.verb} {self.content_object}"
    
    class Meta:
        ordering=['-created_at']

    @property
    def notification_time_formatted(self):
        return self.created_at.strftime("%d %b, %I:%M %p")
    
    def mark_as_read(self):
        self.read=True
        self.save()