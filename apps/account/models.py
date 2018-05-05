from django.contrib.auth.models import User
from core.models import ExModel
from django.db import models


class UserProfile(ExModel):
    """
    Model class for user profile details
    """
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    receive_notifications = models.BooleanField(default=False)

    def __str__(self):
        return "%s" % self.user.name


class ResetPassword(ExModel):
    """
    Model class for forget password storing details
    """
    email = models.EmailField(null=False, blank=False)
    user = models.ForeignKey(User, related_name='reset_password', on_delete=models.CASCADE)
    expired = models.BooleanField(default=False)
    token = models.CharField(null=False, blank=False,max_length=100)

    def __str__(self):
        return "%s" % self.user.name
