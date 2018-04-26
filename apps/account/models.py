from django.contrib.auth.models import User
from core.models import ExModel
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(ExModel):
    """
    Model class for user profile details
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    receive_notifications = models.BooleanField(default=False)

    def __str__(self):
        return "%s" % self.user.name

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.profile.save()
