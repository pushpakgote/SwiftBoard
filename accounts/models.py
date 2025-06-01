from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta,datetime
from django.utils.timesince import timesince
from phonenumber_field.modelfields import PhoneNumberField

#import django signals
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
def profile_image_path_location(instance, filename):
    today_date=datetime.now().strftime("%Y-%m-%d")
    return f"profile/{instance.user.username}/{today_date}/{filename}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='profile')
    job_title=models.CharField(max_length=255, blank=True,null=True)
    profile_picture=models.ImageField(null=True, blank=True, upload_to=profile_image_path_location)
    bio = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=255, blank=True)
    phone=PhoneNumberField(null=True, blank=True,unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    join_date=models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    
    @property
    def profile_picture_url(self):
        try:
            image=self.profile_picture.url
        except:
            image="https://i.pinimg.com/736x/c0/74/9b/c0749b7cc401421662ae901ec8f9f660.jpg"
        return image
    
    @property
    def date_joined(self):
        time_diff=timezone.now()-self.user.date_joined
        if time_diff<=timedelta(days=2):
            return timesince(self.user.date_joined) + " ago"
        else:
            return self.user.date_joined.strftime('%d %b')

    
    # @property
    # def full_name(self):
    #     first_name=self.user.first_name
    #     last_name=self.user.last_name
    #     if first_name and last_name:
    #         return f"{first_name} {last_name}"
    #     return self.user.username

    @property
    def full_name(self):
        name=self.user.get_full_name()
        if name:
            return name
        return self.user.get_username
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, **kwargs):
    Profile.objects.get_or_create(user=instance)

