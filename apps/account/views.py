import logging

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

    @action(methods=['POST'],detail=False)
    def signup(self, request):
        """
        To signup a new user in the system
        :param request:
        :return:
        """
        try:
            if not request.data.get('birthday',None):
                raise err.ValidationError(*("Birthday is not given", 400))
            is_adult(request.data.get('birthday'))
        except Exception as e:
            logger.error(e)
            raise err.ValidationError(*(e, 400))
