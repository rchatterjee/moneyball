"""
Django settings for ffball project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'b-w%e=n_93=p0^2(//yupthisisthething0p!g!x&0k81xl+4jy'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True
TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'ffball/templates')]

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django_admin_bootstrapped.bootstrap3',
    'django_admin_bootstrapped',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social_auth',
#    'social.apps.django_app.default',
    'app',
    'ffball',
    'league', # League page structure
    'data',   # JSON-based data API for AJAX
#    'yahoo'
#    'check_constraints'
)

# django-social-auth settings
FACEBOOK_APP_ID     = '254311618073113'
FACEBOOK_API_SECRET = 'ee2aa55d2ee8a98166d12448d0a3e618'
FACEBOOK_EXTENDED_PERMISSIONS = ['email', 'user_location']
YAHOO_CONSUMER_KEY = 'dj0yJmk9Q0RNYUNNZVBTVGtOJmQ9WVdrOWRIcHhlSGd5TXpnbWNHbzlNVEEwTXpRME9EazJNZy0tJnM9Y29uc3VtZXJzZWNyZXQmeD04Zg--'
YAHOO_CONSUMER_SECRET = 'a002d18b1e30837716aa23aa85f7952aafb7c35d'

AUTHENTICATION_BACKENDS = (
    'social_auth.backends.facebook.FacebookBackend',
    'social_auth.backends.google.GoogleBackend',
    'social_auth.backends.yahoo.YahooBackend',
    'django.contrib.auth.backends.ModelBackend',
)

LOGIN_URL          = '/login-form/'
LOGIN_REDIRECT_URL = '/logged-in/'
LOGIN_ERROR_URL    = '/login-error/'

SOCIAL_AUTH_DEFAULT_USERNAME = 'new_social_auth_user'
SOCIAL_AUTH_UID_LENGTH = 100
SOCIAL_AUTH_ASSOCIATION_HANDLE_LENGTH = 150
SOCIAL_AUTH_NONCE_SERVER_URL_LENGTH = 120
SOCIAL_AUTH_ASSOCIATION_SERVER_URL_LENGTH = 120
SOCIAL_AUTH_USERNAME_IS_FULL_EMAIL = True

SOCIAL_AUTH_PARTIAL_PIPELINE_KEY = 'partial_pipeline'
SOCIAL_AUTH_PIPELINE_RESUME_ENTRY = 'social_auth.backends.pipeline.user.update_user_details'
SOCIAL_AUTH_PIPELINE = (
    'social_auth.backends.pipeline.social.social_auth_user',
    'social_auth.backends.pipeline.user.get_username',
    'social_auth.backends.pipeline.user.create_user',
    'social_auth.backends.pipeline.social.associate_user',
    'social_auth.backends.pipeline.social.load_extra_data',
    'app.pipeline.user.extra_data',
    'social_auth.backends.pipeline.misc.save_status_to_session',
    'app.pipeline.user.session_save',
    'social_auth.backends.pipeline.user.update_user_details',
)

SESSION_SERIALIZER='django.contrib.sessions.serializers.PickleSerializer'

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'social_auth.context_processors.social_auth_by_name_backends',
    'social_auth.context_processors.social_auth_backends',
    'social_auth.context_processors.social_auth_by_type_backends',
    'social_auth.context_processors.social_auth_login_redirect',
    'django.core.context_processors.static',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'ffball.urls'

WSGI_APPLICATION = 'ffball.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'test': {
        'ENGINE': 'django_mysqlpool.backends.mysqlpool',
        'NAME'  : 'srgdb',
        'USER'  : 'saikat',
        'PASSWORD': 'wisc13*tainaki!',
        'HOST' : 'mysql.cs.wisc.edu'
#        'OPTIONS': {
#            'secure-auth': False,
#            }
        },
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME'  : os.path.join(BASE_DIR, 'db.sqlite3'),
        },
#    'mongo_db':{
    #        'ENGINE' : 'django_mongodb_engine',
    #        'NAME' : 'pymongo'
    # }
}

# DATABASE_APP_MAPPING = { 'ffball': 'default', 'yahoo' : 'mongo_db' }
# DATABASE_ROUTERS = ['ffball.db_router.DbRouter']

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
# STATIC_ROOT = '/u/r/c/rchat/moneyball/html/'
STATIC_URL = '/html/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'html/'),
)


