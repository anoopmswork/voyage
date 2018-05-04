# noinspection PyPackageRequirements
import os
import datetime


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ')vc@b)ffcrzhc3gp*59=cxom!8x8es!gki@7kzu%^e1nx*$@_6'
# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT_DIR = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '../../'))
STATIC_ROOT_DIR = os.environ.get('STATIC_ROOT_DIR', PROJECT_ROOT_DIR)
STATIC_URL = '/assets/static/'

STATIC_ROOT = os.path.join(STATIC_ROOT_DIR, 'assets', 'static')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(STATIC_ROOT_DIR, 'assets', 'media')

STATIC_URL = '/static/'

GRAPPELLI_INDEX_DASHBOARD ='voyage.dashboard.CustomIndexDashboard'

GRAPPELLI_ADMIN_TITLE = "Voyage"

JWT_AUTH = {
    'JWT_ENCODE_HANDLER':
    'rest_framework_jwt.utils.jwt_encode_handler',

    'JWT_DECODE_HANDLER':
    'rest_framework_jwt.utils.jwt_decode_handler',

    'JWT_PAYLOAD_HANDLER':
    'rest_framework_jwt.utils.jwt_payload_handler',

    'JWT_PAYLOAD_GET_USER_ID_HANDLER':
    'rest_framework_jwt.utils.jwt_get_user_id_from_payload_handler',

    'JWT_RESPONSE_PAYLOAD_HANDLER':
    'rest_framework_jwt.utils.jwt_response_payload_handler',

    'JWT_SECRET_KEY': SECRET_KEY,
    'JWT_GET_USER_SECRET_KEY': None,
    'JWT_PUBLIC_KEY': None,
    'JWT_PRIVATE_KEY': None,
    'JWT_ALGORITHM': 'HS256',
    'JWT_VERIFY': True,
    'JWT_VERIFY_EXPIRATION': True,
    'JWT_LEEWAY': 0,
    'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=86400),
    'JWT_AUDIENCE': None,
    'JWT_ISSUER': None,

    'JWT_ALLOW_REFRESH': False,
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=7),

    'JWT_AUTH_HEADER_PREFIX': 'JWT',
    'JWT_AUTH_COOKIE': None,

}

AVAILABLE_CHOICES = (
    ('active', 'Active'),
    ('inactive', 'InActive'),
    ('archived', 'Archived'),
)


