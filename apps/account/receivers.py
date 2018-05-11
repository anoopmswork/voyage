import logging
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from core import errors as err
from .models import UserProfile, AuditEntry
from .signals import *

# Get an instance of a logger
logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    try:
        if created:
            UserProfile.objects.create(user=instance)
    except Exception as e:
        logger.error(e)
        raise err.ValidationError(*(e, 400))


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
    try:
        ip = request.META.get('REMOTE_ADDR')
        AuditEntry.objects.create(action='user_logged_in', ip=ip, username=user.username)
    except Exception as e:
        logger.error(e)
        raise err.ValidationError(*(e, 400))


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
    try:
        ip = request.META.get('REMOTE_ADDR')
        AuditEntry.objects.create(action='user_logged_out', ip=ip, username=user.username)
    except Exception as e:
        logger.error(e)
        raise err.ValidationError(*(e, 400))


@receiver(user_login_failed)
def user_login_failed_callback(request, credentials, **kwargs):
    """
    Track user logged out details
    :param sender:
    :param credentials:
    :param kwargs:
    :return:
    """
    try:
        ip = request.META.get('REMOTE_ADDR')
        AuditEntry.objects.create(action='user_login_failed', ip=ip,
                                  username=credentials.get('username', None))
    except Exception as e:
        logger.error(e)
        raise err.ValidationError(*(e, 400))
