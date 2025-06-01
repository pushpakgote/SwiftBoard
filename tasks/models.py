from django.db import models
import uuid
from django.utils import timezone
from django.contrib.auth.models import User
from projects.models import Project

STATUS_CHOICES=[
    ('Backlog','Backlog'),
    ('To Do','To Do'),
    ('In Progress','In Progress'),
    ('Completed','Completed'),
]
STATUS_PRIORITY=[
    ('High','High'),
    ('Medium','Medium'),
    ('Low','Low'),
]
# Create your models here.
class ProjectQuerySet(models.QuerySet):
    def active(self):
        return self.filter(active=True)
    
    def upcomming(self):
        return self.filter(models.Q(due_date__isnull=True) | models.Q(due_date__gte=timezone.now()) )
    
class TaskManager(models.Manager):
    def get_queryset(self):
        return ProjectQuerySet(self.model,using=self._db)
    
    def all(self):
        return self.get_queryset().active().upcomming()
    
class Task(models.Model):
    owner=models.ForeignKey(User,on_delete=models.CASCADE,related_name='tasks')
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    project=models.ForeignKey(Project,on_delete=models.CASCADE,related_name='tasks')
    description = models.TextField(blank=True,null=True)
    status=models.CharField(max_length=20,choices=STATUS_CHOICES,default=STATUS_CHOICES[0][0])
    priority=models.CharField(max_length=20,choices=STATUS_PRIORITY,default=STATUS_PRIORITY[1][0])
    active=models.BooleanField(default=True)
    start_date=models.DateField(blank=True,null=True)
    due_date=models.DateField(blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    objects=TaskManager()

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