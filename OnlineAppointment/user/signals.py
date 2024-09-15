from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Appuser

@receiver(post_save, sender=User)
def create_appuser(sender, instance, created, **kwargs):
    if created:
        # Create an Appuser instance whenever a new User is created
        Appuser.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_appuser(sender, instance, **kwargs):
    instance.appuser.save()