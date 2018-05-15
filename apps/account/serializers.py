from core.serializers import ExModelSerializer
from django.contrib.auth.models import User
from .models import AuditEntry


class UserSerializer(ExModelSerializer):
    class Meta:
        model = User
        exclude = ()


class AuditEntrySerializer(ExModelSerializer):
    class Meta:
        model = AuditEntry
        exclude = ()
