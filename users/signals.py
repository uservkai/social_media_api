from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Profile
from django.contrib.auth import get_user_model

User = get_user_model()

#signal to create profile on new user creation
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        
#signal to save profile on user save
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
