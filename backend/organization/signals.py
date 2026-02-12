from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Department, Team
from django.db import transaction
from django.apps import apps

@receiver(post_save, sender=Team)
def sync_project_managers_on_team_update(sender,instance,created, ** kwargs):
    """
    If team manager changes, update all related project managers atomically.
    """
    if created:
        return # No need to sync on team creation
    
    Project = apps.get_model('work', 'Project')

    if instance.manager:
        
        with transaction.atomic():
            # Update all projects under this team to have the same manager
            Project.objects.filter(team=instance).update(manager=instance.manager)


