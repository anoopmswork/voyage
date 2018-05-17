from django.contrib.auth.models import User
from core.models import ExModel
from django.db import models
from core import helper
from .constants import Gender


class UserProfile(ExModel):
    """
    Model class for user profile details
    """
    GENDER = helper.prop2pair(Gender)
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    receive_notifications = models.BooleanField(default=False)
    gender = models.CharField('Gender', max_length=20, default='male', choices=GENDER)
    native_location = models.TextField(null=False, blank=False)
    bio = models.TextField(null=True, blank=True)
    School = models.TextField(null=True, blank=True)
    Work = models.TextField(null=True, blank=True)
    emergency_contact = models.CharField(max_length=20, null=True, blank=True)
    work_email = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return "%s" % self.user.email


class ResetPassword(ExModel):
    """
    Model class for forget password storing details
    """
    email = models.EmailField(null=False, blank=False)
    user = models.ForeignKey(User, related_name='reset_password', on_delete=models.CASCADE)
    expired = models.BooleanField(default=False)
    token = models.CharField(null=False, blank=False, max_length=100)

    def __str__(self):
        return "%s" % self.user.email


class AuditEntry(ExModel):
    """
    Model class for storing login details
    """
    action = models.CharField(max_length=64)
    ip = models.GenericIPAddressField(null=True)
    username = models.CharField(max_length=256, null=True)

    def __str__(self):
        return '{0} - {1} - {2}'.format(self.action, self.username, self.ip)
