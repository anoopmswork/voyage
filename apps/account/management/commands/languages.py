"""
=========
syncperms
=========
This command fill the languages in the database
"""
import requests, json, logging

from django.core.management.base import BaseCommand, CommandError
from apps.account.models import Languages, Notification
from core import helper, errors as err
from django.contrib.auth.models import User


# Get an instance of a logger
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def add_languages(self):
        try:
            url = 'https://pkgstore.datahub.io/core/language-codes/language-codes_json/data/734c5eea7e10548144a18241e8f931f8/language-codes_json.json'
            result = requests.get(url=url)
            formatted_result = json.loads(result.text)
            for lang in formatted_result:
                Languages.objects.create(code=lang.get('alpha2', None), name=lang.get('English', None))
        except Exception as e:
            logger.error(e)
            raise err.ValidationError(*(e, 400))

    def add_notifications(self):
        try:
            from apps.account.constants import NotificationTypes
            NotificationTypes = helper.prop2pair(NotificationTypes)
            for individual_user in User.objects.all():
                if Notification.objects.filter(user=individual_user).count() == 0:
                    for k, v in NotificationTypes:
                        Notification.objects.create(user=individual_user, notification_type=k)
        except Exception as e:
            logger.error(e)
            raise err.ValidationError(*(e, 400))

    def handle(self, *args, **options):
        self.add_languages()
        self.add_notifications()
