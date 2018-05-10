from django.apps import AppConfig
from django.dispatch import Signal



class AccountConfig(AppConfig):
    name = 'apps.account'

    def ready(self):
        from . import receivers
