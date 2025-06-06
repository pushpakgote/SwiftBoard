from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Team(models.Model):
    name = models.CharField(max_length=100,unique=True)
    description = models.TextField(null=True,blank=True)
    team_lead = models.ForeignKey(User, on_delete=models.CASCADE,related_name='team_lead')
    members = models.ManyToManyField(User,related_name='teams')
    created_by=models.ForeignKey(User, on_delete=models.CASCADE,related_name='created_teams')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-created_at']