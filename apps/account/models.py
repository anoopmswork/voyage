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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    receive_notifications = models.BooleanField(default=False)
    gender = models.CharField('Gender', max_length=20, default='male', choices=GENDER)
    native_location = models.TextField(default='Delhi', null=False, blank=False)
    bio = models.TextField(null=True, blank=True)
    School = models.TextField(null=True, blank=True)
    Work = models.TextField(null=True, blank=True)
    emergency_contact = models.CharField(max_length=20, null=True, blank=True)
    work_email = models.CharField(max_length=100, null=True, blank=True)
    dob = models.CharField('DOB', max_length=20, null=True, blank=True)
    preferred_language = models.CharField('Language', max_length=100, default='English')
    preferred_currency = models.CharField('Currency', max_length=100, default='Indian rupee')
    time_zone = models.CharField('Time Zone', max_length=100, default='(UTC +5:30)')
    languages = models.TextField(null=True, blank=True)
    vat_number = models.CharField(max_length=100, null=True, blank=True)
    emergency_contact = models.TextField(null=True, blank=True)
    shipping_address = models.TextField(null=True, blank=True)
    guest_profiles = models.TextField(null=True, blank=True)

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


class PhoneNumber(ExModel):
    """
    Model class for storing phone number details
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    number = models.CharField(max_length=100)
    verified = models.BooleanField(default=False)


class Languages(ExModel):
    """
    Model class for storing language details
    """
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class UserLanguages(ExModel):
    """
    Model class for storing user language details
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    language = models.ForeignKey(Languages, on_delete=models.CASCADE)
