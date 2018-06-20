"""
=========
syncperms
=========
This command fill the languages in the database
"""
import requests, json

from django.core.management.base import BaseCommand, CommandError
from apps.account.models import Languages


class Command(BaseCommand):
    def add_languages(self):
        url = 'https://pkgstore.datahub.io/core/language-codes/language-codes_json/data/734c5eea7e10548144a18241e8f931f8/language-codes_json.json'
        result = requests.get(url=url)
        formatted_result = json.loads(result.text)

    def handle(self, *args, **options):
        self.add_languages()
