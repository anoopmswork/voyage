import logging
import string
import random
import requests
import json
import pytz

from core.viewsets import ExModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import permission_classes, action
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate, logout
from rest_framework_jwt.settings import api_settings
from core import errors as err
from rest_framework import status, viewsets
from django.contrib.auth.models import User
from .utils import is_adult
from django.contrib.auth.hashers import make_password, check_password
from post_office import mail
from .models import ResetPassword, AuditEntry, \
    UserProfile, Languages, UserLanguages, VatVerification, \
    EmergencyContact, ShippingAddress, GuestProfile
from datetime import datetime, timedelta
from django.utils import timezone
from .signals import user_logged_in, user_logged_out, \
    user_login_failed
from django.contrib.auth import logout
from .serializers import AuditEntrySerializer, \
    UserProfileSerializer, UserSerializer, \
    UserProfileCreateSerializer, LanguagesSerializer, \
    UserLanguagesSerializer, VatVerificationSerializer, \
    VatVerificationCreateSerializer, EmergencyContactSerializer, \
    EmergencyContactCreateSerializer
from . import serializers

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

# Get an instance of a logger
logger = logging.getLogger(__name__)


@permission_classes((AllowAny,))
class AccountViewSet(ExModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    retrieve_serializer_class = UserSerializer

    def random_word(self, length):
        try:
            letters = string.ascii_lowercase
            return ''.join(random.choice(letters) for i in range(length))
        except Exception as e:
            logger.error(e)
            raise err.ValidationError(*(e, 400))

    def verify_birthday(self, birthday=None):
        """
        Verify birthday to find whether adult or not
        :param birthday:
        :return:
        """
        try:
            if not birthday:
                raise err.ValidationError(*("Birthday is not given", 400))
            if not is_adult(birthday):
                raise err.ValidationError(*("You are not an adult", 400))
        except Exception as e:
            logger.error(e)
            raise err.ValidationError(*(e, 400))

    def verify_password(self, **params):
        try:
            if not params['first_name'] or not params['last_name']:
                raise err.ValidationError(*("First name and last name cant be empty", 400))
            if len(params['password']) < 9:
                raise err.ValidationError(*("At least 8 characters", 400))
            invalid_chars = set(string.punctuation.replace("_", ""))
            if not any(char.isdigit() for char in params['password']) \
                    and not any(char in invalid_chars for char in params['password']):
                raise err.ValidationError(*("Must contains a number or symbol", 400))
            if params['first_name'] in params['password'] \
                    or params['last_name'] in params['password'] or \
                            params['email'] in params['password']:
                raise err.ValidationError(*("Password cannot contain your name or email address", 400))
        except Exception as e:
            logger.error(e)
            raise err.ValidationError(*(e, 400))

    @action(methods=['POST'], detail=False)
    def signup(self, request):
        """
        To signup a new user in the system
        :param request:
        :return:
        """
        try:
            self.verify_birthday(request.data.get('birthday', None))
            first_name = request.data.get('first_name', None)
            last_name = request.data.get('last_name', None)
            email = request.data.get('email', None)
            password = request.data.get('password', None)
            username = request.data.get('username', None)
            params = {
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'password': make_password(password),
                'username': username
            }
            self.verify_password(**params)
            serializer = UserSerializer(data=params)
            if serializer.is_valid(raise_exception=True):
                user = serializer.save()
            return Response({"success": True,
                             "msg": "User successfully registered"})
        except Exception as e:
            logger.error(e)
            raise err.ValidationError(*(e, 400))

    @action(methods=['POST'], detail=False)
    def login(self, request):
        """
        To authenticate a user login
        :param request:
        :return:
        """
        try:
            username = request.data.get('email', None)
            password = request.data.get('password', None)
            if username is None or password is None:
                raise err.ValidationError(*("Email or password is not given", 400))
            user = authenticate(username=username, password=password)
            if user is not None:
                payload = jwt_payload_handler(user)
                token = jwt_encode_handler(payload)
                user_logged_in.send(sender=User, request=request, user=user)
                return Response({
                    "token": token,
                    "status": "success",
                })
            else:
                user_login_failed.send(None, request=request, credentials={'username': username})
                return Response({
                    "status": "failure",
                    "msg": "Invalid parameters"
                })
        except Exception as e:
            logger.error(e)
            raise err.ValidationError(*(e, 400))

    @action(methods=['POST'], detail=False)
    def forget_password(self, request):
        """
        To reset password for forget password functionality
        :param request:
        :return:
        """
        try:
            email = request.data.get('email', None)
            if not email:
                raise err.ValidationError(*("Email  is not given", 400))
            user = User.objects.filter(email=email).first()
            if not user:
                raise err.ValidationError(*("User does not exist for this given email", 400))
            token = self.random_word(8)
            ResetPassword.objects.create(email=email, user=user, token=token)
            link = request.get_host() + "/reset_password?token=" + token
            mail.send(
                email,  # List of email addresses also accepted
                'anoopmsfreelancer@gmail.com',
                template='forget_password',  # Could be an EmailTemplate instance or name
                context={'user': user.first_name, 'link': link},
                priority='now',
            )
            return Response({"success": True,
                             "msg": "Reset password link is "
                                    "successfully send to your email"})
        except Exception as e:
            logger.error(e)
            raise err.ValidationError(*(e, 400))

    @action(methods=['POST'], detail=False)
    def reset_password(self, request):
        """
        To reset forget password with new password
        :param request:
        :return:
        """
        try:
            token = request.query_params.get('token', None)
            password = request.data.get('password', None)
            reset_password = ResetPassword.objects.filter(token=token).first()
            if reset_password and (timezone.now() - reset_password.created_at).days > 0 or reset_password.expired:
                raise err.ValidationError(*("Reset password link is expired", 400))
            if check_password(password, reset_password.user.password) or not password:
                raise err.ValidationError(*("New password cant be the old password or empty", 400))
            params = {
                'first_name': reset_password.user.first_name,
                'last_name': reset_password.user.last_name,
                'email': reset_password.user.email,
                'password': make_password(password),
                'username': reset_password.user.username
            }
            self.verify_password(**params)
            reset_password.user.set_password(password)
            reset_password.user.save()
            ResetPassword.objects.filter(user=reset_password.user).exclude(pk=reset_password.pk).all().delete()
            reset_password.expired = True
            reset_password.save()
            return Response({"success": True,
                             "msg": "Password successfully changed"})
        except Exception as e:
            logger.error(e)
            raise err.ValidationError(*(e, 400))


class UserViewSet(ExModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    retrieve_serializer_class = UserSerializer

    @action(methods=['POST'], detail=False)
    def change_password(self, request):
        """
        To change password of an existing user
        :param request:
        :return:
        """
        try:
            new_password = request.data.get('new_password', None)
            old_password = request.data.get('old_password', None)
            if not new_password or not old_password:
                raise err.ValidationError(*("Password details are not entered", 400))
            if check_password(old_password, request.user.password):
                request.user.set_password(new_password)
                request.user.save()
                return Response({"success": True,
                                 "msg": "Password successfully changed"})
            else:
                raise err.ValidationError(*("Current password is false", 400))
        except Exception as e:
            logger.error(e)
            raise err.ValidationError(*(e, 400))

    @action(methods=['POST'], detail=False)
    def logout(self, request):
        """
        To change password of an existing user
        :param reques
        :return:
        """
        try:
            # TODO
            url = "http://" + request.get_host() + "/api-token-refresh/"
            post_data = {
                "token": request.auth.decode("utf-8")
            }
            headers = {
                'Content-Type': 'application/json'
            }
            result = requests.post(url=url, headers=headers, data=post_data)
            user_logged_out.send(sender=User, request=request, user=request.user)
            logout(request)
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(e)
            raise err.ValidationError(*(e, 400))

    @action(methods=['GET'], detail=False)
    def attempts(self, request):
        """
        To list audit login details for a user
        :param request:
        :return:
        """
        try:
            audit_entries = AuditEntry.objects.filter(username=request.user.username).order_by('-created_at')[:5]
            serialized_data = AuditEntrySerializer(audit_entries, many=True).data
            return Response({"data": serialized_data})
        except Exception as e:
            logger.error(e)
            raise err.ValidationError(*(e, 400))


class UserProfileViewSet(ExModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    create_serializer_class = UserProfileCreateSerializer
    update_serializer_class = UserProfileCreateSerializer

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete(force=True)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            logger.error(e)
            raise err.ValidationError(*(e, 400))



class GeoViewSet(viewsets.ViewSet):
    """
    A simple viewset for listing geo,language,currencies etc
    """

    @action(methods=['GET'], detail=False)
    def currencies(self, request):
        try:
            url = 'https://openexchangerates.org/api/currencies.json'
            result = requests.get(url=url)
            return Response({"data": json.loads(result.text)})
        except Exception as e:
            logger.error(e)
            raise err.ValidationError(*(e, 400))

    @action(methods=['GET'], detail=False)
    def languages(self, request):
        try:
            languages = Languages.objects.all()
            return Response({"data": LanguagesSerializer(languages, many=True).data})
        except Exception as e:
            logger.error(e)
            raise err.ValidationError(*(e, 400))

    @action(methods=['GET'], detail=False)
    def phone_codes(self, request):
        try:
            url = 'https://gist.githubusercontent.com/Goles/3196253/raw/9ca4e7e62ea5ad935bb3580dc0a07d9df033b451/CountryCodes.json'
            result = requests.get(url=url)
            return Response({"data": json.loads(result.text)})
        except Exception as e:
            logger.error(e)
            raise err.ValidationError(*(e, 400))

    @action(methods=['GET'], detail=False)
    def time_zones(self, request):
        try:
            timezones = pytz.all_timezones
            return Response({"data": timezones})
        except Exception as e:
            logger.error(e)
            raise err.ValidationError(*(e, 400))

    @action(methods=['POST'], detail=False)
    def add_user_language(self, request):
        try:
            user = request.user
            language = Languages.objects.filter(pk=request.data.get('language', None)).first()
            user_language = UserLanguages.objects.create(user=user, language=language)
            return Response({"data": UserLanguagesSerializer(user_language).data})
        except Exception as e:
            logger.error(e)
            raise err.ValidationError(*(e, 400))

    @action(methods=['GET'], detail=False)
    def list_user_languages(self, request):
        try:
            user_languages = UserLanguages.objects.filter(user=request.user).all()
            return Response({"data": UserLanguagesSerializer(user_languages, many=True).data})
        except Exception as e:
            logger.error(e)
            raise err.ValidationError(*(e, 400))

    @action(methods=['POST'], detail=False)
    def delete_user_language(self, request):
        try:
            user_language_id = request.data.get('user_language_id', None)
            UserLanguages.objects.filter(pk=user_language_id).first().delete(force=True)
            return Response({"data": "Success"})
        except Exception as e:
            logger.error(e)
            raise err.ValidationError(*(e, 400))

    @action(methods=['GET'], detail=False)
    def countries(self, request):
        try:
            url = 'http://country.io/names.json'
            result = requests.get(url=url)
            return Response({"data": json.loads(result.text)})
        except Exception as e:
            logger.error(e)
            raise err.ValidationError(*(e, 400))


class VatViewSet(ExModelViewSet):
    """
    Viewset forshowing userprofile details
    """
    queryset = VatVerification.objects.all()
    serializer_class = VatVerificationSerializer
    create_serializer_class = VatVerificationCreateSerializer


class EmergencyContactViewSet(ExModelViewSet):
    """
    Viewset for showing userprofile details
    """
    queryset = EmergencyContact.objects.all()
    serializer_class = EmergencyContactSerializer
    create_serializer_class = EmergencyContactCreateSerializer


class ShippingContactViewSet(ExModelViewSet):
    """
    Viewset for showing shipping contact details
    """
    queryset = ShippingAddress.objects.all()
    serializer_class = serializers.ShippingAddressSerializer
    create_serializer_class = serializers.ShippingAddressCreateSerializer


class GuestProfileViewSet(ExModelViewSet):
    """
    Viewset for showing guest profile details
    """
    queryset = GuestProfile.objects.all()
    serializer_class = serializers.GuestProfileSerializer
    create_serializer_class = serializers.GuestProfileCreateSerializer
