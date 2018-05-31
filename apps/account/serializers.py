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
        exclude = ('user',)

    def validate(self, attrs):
        return attrs

    def create(self, validated_data):
        try:
            validated_data['user'] = self.context['request'].user.pk
            userprofile_serializer = UserProfileSerializer(data=validated_data)
            if userprofile_serializer.is_valid(raise_exception=True):
                userprofile = userprofile_serializer.save()
            return userprofile
        except Exception as e:
            logger.error(e)
            raise err.ValidationError(*(e, 400))

    def update(self, instance, validated_data):
        try:
            validated_data['user'] = self.context['request'].user.pk
            userprofile_serializer = UserProfileSerializer(instance,
                                                           data=validated_data, partial=True)
            if userprofile_serializer.is_valid(raise_exception=True):
                userprofile = userprofile_serializer.save()
            return userprofile
        except Exception as e:
            logger.error(e)
            raise err.ValidationError(*(e, 400))
