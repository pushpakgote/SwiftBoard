from django.db import models
import uuid
from django.utils import timezone
from datetime import timedelta,datetime
from django.contrib.auth.models import User
from teams.models import Team
from .utils import STATUS_CHOICES,STATUS_PRIORITY


# Create your models here.
class ProjectQuerySet(models.QuerySet):
    def active(self):
        return self.filter(active=True)
    
    def upcomming(self):
        return self.filter(due_date__gte=timezone.now())
    
    def due_in_two_days_or_less(self):
        today=timezone.now().date()
        two_days_from_today=today+timedelta(days=2)
        return self.active().upcomming().filter(due_date__lte=two_days_from_today)
    
class ProjectManager(models.Manager):
    def get_queryset(self):
        return ProjectQuerySet(self.model,using=self._db)
    
    def all(self):
        return self.get_queryset().active().upcomming()
    
    def due_in_two_days_or_less(self):
        return self.get_queryset().due_in_two_days_or_less()

class Project(models.Model):
    owner=models.ForeignKey(User,on_delete=models.CASCADE,related_name='projects')
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    team=models.ForeignKey(Team,on_delete=models.SET_NULL,null=True,blank=True,related_name='projects')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True,null=True)
    client_company=models.CharField(max_length=100,blank=True,null=True)
    status=models.CharField(max_length=20,choices=STATUS_CHOICES,default=STATUS_CHOICES[0][0])
    priority=models.CharField(max_length=20,choices=STATUS_PRIORITY,default=STATUS_PRIORITY[1][0])

    # Budget Details
    total_amount=models.DecimalField(max_digits=10,decimal_places=2,blank=True,null=True)
    amount_spent=models.DecimalField(max_digits=10,decimal_places=2, default=0.00,blank=True,null=True)
    estimated_duration=models.IntegerField(blank=True,null=True, help_text="Estimated duration in days")

    active=models.BooleanField(default=True)
    start_date=models.DateField()
    due_date=models.DateField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    objects=ProjectManager()

    def __str__(self):
        return self.name
    
    class Meta:
        ordering=['-created_at']
    
    def days_until_due(self):
        if self.due_date:
            current_date=timezone.now().date()
            return (self.due_date - current_date).days
        return None
    
    @property
    def progress(self):
        progress_dict={
            'To Do':0,
            'In Progress':50,
            'Completed':100,
        }
        return progress_dict.get(self.status,0)
    
    @property
    def status_color(self):
        status_value=self.progress
        if status_value==100:
            return 'success'
        elif status_value==50:
            return 'primary'
        else:
            return ''
    
    def priority_color(self):
        if self.priority=='High':
            return 'danger'
        elif self.priority=='Medium':
            return 'warning'
        else:
            return 'success'
        
#Project file location
def profile_attachment_path_location(instance, filename):
    today_date=datetime.now().strftime("%Y-%m-%d")
    return f"attachments/{instance.project.name}/{today_date}/{filename}"

class Attachment(models.Model):
    project=models.ForeignKey(Project,on_delete=models.CASCADE,related_name='attachments')
    user=models.ForeignKey(User, on_delete=models.CASCADE,related_name='attachments')
    file=models.FileField(upload_to=profile_attachment_path_location)
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Attachment by {self.user.username} on {self.project.name}"
    
    def get_attachment_name(self):
        return self.file.name.split('/')[-1]