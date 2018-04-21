"""
======
Errors
======
This module holds exceptions for all other app
"""
from django.utils.translation import ugettext as _

from rest_framework import exceptions


class Messages(object):
    """
    Helper class to hold error message and its for each app

    Error code is consist of 2 digit prefix which indicates the app and the 2 digits error code
    """
    #: System wide unexpected error
    UNEXPECTED = _('Unexpected error occurred'), -1
    UPLOAD_USER_MISMATCH = _('You cannot upload files behalf of the other user')

    # Account app, prefixed with 10
    EMAIL_EXIST = _("Email address already exists"), 1001





    class Validation(object):
        INVALID_STATE = _('Invalid US state abbreviation')


class APIException(exceptions.APIException):
    """
    Exception class that caught by renderer and produce pretty output.

    It also has ``error_code`` attribute that may be set by other app otherwise it'll be ``-1``
    """

    def __init__(self, detail=None, error_code=-1, kw=None):
        if isinstance(kw, dict):
            detail = detail % kw
        super(APIException, self).__init__(detail=detail)
        self.error_code = error_code
        self.message = detail


class ValidationError(APIException):
    """
    Exception class for all kind of validation errors
    """
    status_code = 400


class NotFound(APIException):
    """
    Exception class for missing resource
    """
    status_code = 404


class UserError(APIException):
    status_code = 400


class StaticFileError(APIException):
    status_code = 400


class AuthorizationError(APIException):
    status_code = 401


class IntegrationError(APIException):
    status_code = 700


m = Messages
vm = Messages.Validation
