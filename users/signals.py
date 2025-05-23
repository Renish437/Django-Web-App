from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import Profile
from django.shortcuts import get_object_or_404

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        # Create the profile and link it to the user
        Profile.objects.create(
            user=instance,
            email=instance.email,  # You can add more fields if needed
        )
    else:
        profile = get_object_or_404(Profile, user=instance)
        profile.email = instance.email
        profile.save()
   
@receiver(post_save, sender=Profile)     
def update_user(sender, instance, created, **kwargs):
    if created == False:
        user = get_object_or_404(User,id=instance.user.id)
        if user.email != instance.email:
            user.email = instance.email
            user.save()
        


