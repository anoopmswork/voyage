import json

from braces.views import CsrfExemptMixin
from django.conf import settings
from django.http import HttpResponse
from eventcalendar.models import CredentialsModel, \
    EventGoogleCalendar
from oauth2_provider.settings import oauth2_settings
from oauth2_provider.views.mixins import OAuthLibMixin
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rocketchat.utils import get_rocket_chat_token, logout_rocket_chat, check_rocket_token

from apps.account import ContactRefSerializer, SignUpSerializer, ResetPasswordSerializer
from apps.account import User, Invitations
from core import errors as err


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


class TokenView(APIView, CsrfExemptMixin, OAuthLibMixin):
    permission_classes = (AllowAny,)
    authentication_classes = (CsrfExemptSessionAuthentication,)
    server_class = oauth2_settings.OAUTH2_SERVER_CLASS
    validator_class = oauth2_settings.OAUTH2_VALIDATOR_CLASS
    oauthlib_backend_class = oauth2_settings.OAUTH2_BACKEND_CLASS

    def delete_calendar_credentials(self, user):
        CredentialsModel.objects.filter(pk=user.id).delete()
        EventGoogleCalendar.objects.filter(user=user).delete()

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        grant_type = request.POST.get('grant_type')

        try:
            if username is None:
                raise User.DoesNotExist
            user = User.objects.get(email=username)
            # Deleting existing user token for our web client application
            # If enbaled it will logout all other active web browser logins
            # AccessToken.objects.filter(user=user, application=Application.objects.get(name="Web Client")).delete()
        except Exception as e:
            raise err.ValidationError(*err.m.EMAIL_NOT_EXISTS)

        self.delete_calendar_credentials(user)

        url, headers, body, status_code = self.create_token_response(request)

        if status_code == 200:
            token = json.loads(body)
            token['rocket_chat'] = get_rocket_chat_token(user)
            token['contact'] = ContactRefSerializer(user.get_contact_profile, many=False).data
            token = json.dumps(token)
        else:
            raise err.ValidationError(*err.m.PASSWORD_WRONG)

        response = HttpResponse(content=token, status=status_code)

        for k, v in headers.items():
            response[k] = v
        return response


class InvitationTokenCheck(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def get(self, request, token):
        try:
            invitation = Invitations.objects.get(reference=token)

            if invitation.is_accepted:
                raise err.ValidationError(*err.m.INVALID_URL)
            else:
                status_code = status.HTTP_200_OK
                content = {'status': 'Valid', 'email': invitation.contact.email}
                response = dict(data=content)
                content = json.dumps(response)

        except:
            raise err.ValidationError(*err.m.INVALID_URL)

        response = HttpResponse(content=content, status=status_code)
        return response


class UserRegistration(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def post(self, request, format=None):
        """
        Register new user with key
        :param str password: Password\n
        :param str first_name: First name\n
        :param str last_name: Last Name\n
        :param str invitation_ref: Invitation Token
        """
        try:
            serializer = SignUpSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            values = {"status": "Success"}
            response = dict(data=values)
            return Response(response, status=status.HTTP_201_CREATED)
        except Exception as e:
            raise err.ValidationError(*err.m.INVALID_DATA)


class ResetPassword(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def post(self, request, format=None):
        """
        Generates password reset key and send email

        :param str email: Email address
        """
        try:
            User.objects.generate_password_reset_key(request.data.get('email'))
            values = {"status": "Success"}
            return Response(dict(data=values), status=status.HTTP_201_CREATED)
        except Exception as e:
            raise err.ValidationError(*err.m.EMAIL_NOT_EXISTS)

    def put(self, request, format=None):
        """
        Reset Password request with password reset key

        :param str email: Email address
        :param str reset_key: Password Rest Key
        :param str new_password: New Password
        """
        try:
            serializer = ResetPasswordSerializer(data=request.data)
            serializer.is_valid(True)
            User.objects.reset_password(**serializer.data)
            values = {"status": "Success"}
            return Response(dict(data=values), status=status.HTTP_201_CREATED)
        except Exception as e:
            raise err.ValidationError(*err.m.INVALID_URL)


class FeedbackMail(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def post(self, request, format=None):
        """
        Generates password reset key and send email

        :param str email: Email address
        """
        from core import Email
        try:
            data = dict(
                    website=request.POST.get('website', 'web'),
                    type=request.POST.get('type', 'request'),
                    name=request.POST.get('name', 'Anonymous'),
                    email=request.POST.get('email', 'Anonymous email'),
                    subject=request.POST.get('subject', 'No Subject'),
                    message=request.POST.get('message', 'No message'),
            )
            Email.send('contact-request-notification-admin', settings.FEEDBACK_EMAIL, data)
            return Response(dict(data=data), status=status.HTTP_201_CREATED)
        except Exception as e:
            raise err.ValidationError(*err.m.INVALID_DATA)


class TokenLogoutView(APIView, CsrfExemptMixin, OAuthLibMixin):
    authentication_classes = (CsrfExemptSessionAuthentication,)
    server_class = oauth2_settings.OAUTH2_SERVER_CLASS
    validator_class = oauth2_settings.OAUTH2_VALIDATOR_CLASS
    oauthlib_backend_class = oauth2_settings.OAUTH2_BACKEND_CLASS

    def delete_calendar_credentials(self, user):
        CredentialsModel.objects.filter(pk=user.id).delete()
        EventGoogleCalendar.objects.filter(user=user).delete()

    def post(self, request):
        self.delete_calendar_credentials(request.user)
        logout_rocket_chat(request)
        url, headers, body, status_code = self.create_revocation_response(request)
        if status_code == 200:

            response = HttpResponse(content='', status=status_code)
            return response
        else:
            raise err.ValidationError(*err.m.PASSWORD_WRONG)


class RocketTokenCheck(APIView, CsrfExemptMixin, OAuthLibMixin):
    authentication_classes = (CsrfExemptSessionAuthentication,)
    server_class = oauth2_settings.OAUTH2_SERVER_CLASS
    validator_class = oauth2_settings.OAUTH2_VALIDATOR_CLASS
    oauthlib_backend_class = oauth2_settings.OAUTH2_BACKEND_CLASS

    def post(self, request):
        result = check_rocket_token(request)
        if result.status_code != 200:
            self.create_revocation_response(request)
        return Response(dict(status=result.status_code), status=status.HTTP_200_OK)
