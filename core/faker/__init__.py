__all__ = ['fake']

from faker.providers import BaseProvider
from faker import Factory
from event.models import Event
from system.models import ParameterEnum

fake = Factory.create(locale='en_US')


class EventProvider(BaseProvider):
    @classmethod
    def service(cls):
        return Event.objects.order_by('?').first()

    def service_id(self):
        return self.event().id


class EnumProvider(BaseProvider):
    @classmethod
    def enum(cls, enum):
        return ParameterEnum.objects.filter(enum=enum).order_by('?').first()

    def enum_id(self, enum):
        return self.enum(enum).id




fake.add_provider(EventProvider)
fake.add_provider(EnumProvider)
