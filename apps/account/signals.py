from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserProfile, AuditEntry
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):
    """
    Track user login details
    :param sender:
    :param request:
    :param user:
    :param kwargs:
    :return:
    """
    ip = request.META.get('REMOTE_ADDR')
    AuditEntry.objects.create(action='user_logged_in', ip=ip, username=user.username)


@receiver(user_logged_out)
def user_logged_out_callback(sender, request, user, **kwargs):
    """
    Track user logged out details
    :param sender:
    :param request:
    :param user:
    :param kwargs:
    :return:
    """
    ip = request.META.get('REMOTE_ADDR')
    AuditEntry.objects.create(action='user_logged_out', ip=ip, username=user.username)


@receiver(user_login_failed)
def user_login_failed_callback(sender, credentials, **kwargs):
    """
    Track user logged out details
    :param sender:
    :param credentials:
    :param kwargs:
    :return:
    """
    AuditEntry.objects.create(action='user_login_failed', username=credentials.get('username', None))
