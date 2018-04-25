import logging

from core.viewsets import ExModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import permission_classes,action
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate, logout
from rest_framework_jwt.settings import api_settings
from core import errors as err
from rest_framework import status,viewsets

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.
