from celery import shared_task
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Notification
from projects.models import Project

@shared_task
def create_notification(actor_username, verb,object_id):
    try:
        actor = User.objects.get(username=actor_username)
        project=Project.objects.get(id=object_id)
        #get members
        members=project.team.members.exclude(id=project.owner.id)
        for recipient in members:
            notification=Notification.objects.create(
                        actor=actor,
                        recipient=recipient,
                        verb=verb,
                        content_object=project,
                        read=False
                    )
        return notification.verb
    except User.DoesNotExist:
        return None
    
@shared_task
def notify_team_due_project_tasks():
    project_due_soon=Project.objects.due_in_two_days_or_less()
    for project in project_due_soon:
        verb=f'Reminder: Project Due Soon, {project.name}'
        actor_username=project.owner.username
        members=project.team.members.all()
        for recipient in members:
            create_notification.delay(actor_username=actor_username, verb=verb,object_id=project.id)