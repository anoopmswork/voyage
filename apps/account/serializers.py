import logging
from core.serializers import ExModelSerializer
from django.contrib.auth.models import User
from .models import AuditEntry, UserProfile
from core import errors as err

# Get an instance of a logger
logger = logging.getLogger(__name__)


class UserSerializer(ExModelSerializer):
    class Meta:
        model = User
        exclude = ()


class AuditEntrySerializer(ExModelSerializer):
    class Meta:
        model = AuditEntry
        exclude = ()


class UserProfileSerializer(ExModelSerializer):
    class Meta:
        model = UserProfile
        exclude = ()


class UserProfileCreateSerializer(ExModelSerializer):
    class Meta:
        model = UserProfile
        exclude = ()

    def validate(self, attrs):
        return attrs

    def create(self, validated_data):
        try:
            userprofile_serializer = UserProfileSerializer(data=validated_data)
            if userprofile_serializer.is_valid(raise_exception=True):
                userprofile = userprofile_serializer.save()
            return userprofile
        except Exception as e:
            logger.error(e)
            raise err.ValidationError(*(e, 400))
