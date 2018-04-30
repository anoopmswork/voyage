import logging
import string
from core.viewsets import ExModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import permission_classes, action
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate, logout
from rest_framework_jwt.settings import api_settings
from core import errors as err
from rest_framework import status, viewsets
from django.contrib.auth.models import User
from .serializers import UserSerializer
from .utils import is_adult

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

# Get an instance of a logger
logger = logging.getLogger(__name__)


@permission_classes((AllowAny,))
class AccountViewSet(ExModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    retrieve_serializer_class = UserSerializer

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
            if len(params['password']) < 9:
                raise err.ValidationError(*("At least 8 characters", 400))
            invalid_chars = set(string.punctuation.replace("_", ""))
            if not any(char.isdigit() for char in params['password']) \
                    and not any(char in invalid_chars for char in params['password']):
                raise err.ValidationError(*("Must contains a number or symbol", 400))
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
            params = {
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'password': password
            }
            self.verify_password(**params)
            print("test")
        except Exception as e:
            logger.error(e)
            raise err.ValidationError(*(e, 400))
