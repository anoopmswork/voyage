"""
=========
syncperms
=========
This command fill the languages in the database
"""
import requests, json,logging

from django.core.management.base import BaseCommand, CommandError
from apps.account.models import Languages
from core import errors as err

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


    def handle(self, *args, **options):
        self.add_languages()
