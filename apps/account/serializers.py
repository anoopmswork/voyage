import logging
from core.serializers import ExModelSerializer
from django.contrib.auth.models import User
from .models import AuditEntry, UserProfile, Languages, \
    UserLanguages, VatVerification, EmergencyContact
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


class LanguagesSerializer(ExModelSerializer):
    class Meta:
        model = Languages
        exclude = ()


class UserLanguagesSerializer(ExModelSerializer):
    class Meta:
        model = UserLanguages
        exclude = ()


class VatVerificationSerializer(ExModelSerializer):
    class Meta:
        model = VatVerification
        exclude = ()


class VatVerificationCreateSerializer(ExModelSerializer):
    class Meta:
        model = VatVerification
        exclude = ('user',)

    def create(self, validated_data):
        try:
            validated_data['user'] = self.context['request'].user.pk
            vat_serializer = VatVerificationSerializer(data=validated_data)
            if vat_serializer.is_valid(raise_exception=True):
                vat_verification = vat_serializer.save()
            return vat_verification
        except Exception as e:
            logger.error(e)
            raise err.ValidationError(*(e, 400))


class EmergencyContactSerializer(ExModelSerializer):
    class Meta:
        model = EmergencyContact
        exclude = ()


class EmergencyContactCreateSerializer(ExModelSerializer):
    class Meta:
        model = EmergencyContact
        exclude = ('user',)

    def create(self, validated_data):
        try:
            validated_data['user'] = self.context['request'].user.pk
            emergency_contact_serializer = EmergencyContactSerializer(data=validated_data)
            if emergency_contact_serializer.is_valid(raise_exception=True):
                emergency_contact = emergency_contact_serializer.save()
            return emergency_contact
        except Exception as e:
            logger.error(e)
            raise err.ValidationError(*(e, 400))
