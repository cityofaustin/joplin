"""
Django settings for joplin project.

Generated by 'django-admin startproject' using Django 1.11.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import logging
from distutils.util import strtobool
from urllib.parse import urlparse

import dj_database_url
from django.conf import global_settings

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(PROJECT_DIR)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/


DEBUG = bool(strtobool(os.environ.get('DEBUG', str(False))))
MODELTRANSLATION_DEBUG = DEBUG
USE_ANALYTICS = bool(
    strtobool(os.environ.get('USE_ANALYTICS', str(not DEBUG))))


# Application definition

INSTALLED_APPS = [
    'base.apps.BaseConfig',
    'users',
    'api.apps.APIConfig',

    'wagtail.api.v2',

    'wagtail_react_streamfield',
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtail.core',
    'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    'wagtail.contrib.styleguide',
    'wagtail.contrib.settings',
    'wagtail_modeltranslation',
    'wagtail_modeltranslation.makemigrations',
    'wagtail_modeltranslation.migrate',

    'modelcluster',
    'taggit',
    'rest_framework',
    'rest_framework_api_key',
    'corsheaders',
    'modeltranslation',
    'graphene_django',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'django.contrib.admindocs',
    'wagtail.contrib.modeladmin',
    'webpack_loader',
    'dbbackup',
    'smuggler',

    'session_security',
    'phonenumber_field',
    'countable_field',
    'flags',
    'silk',
    'gql',

    'groups',
    'publish_preflight',
    'pages',
    'pages.base_page',
    'pages.department_page',
    'pages.event_page',
    'pages.form_container',
    'pages.guide_page',
    'pages.information_page',
    'pages.location_page',
    'pages.official_documents_page',
    'pages.official_documents_collection',
    'pages.service_page',
    'pages.topic_collection_page',
    'pages.topic_page',
    'pages.home_page',
    'pages.news_page',
    'snippets.contact',
    'snippets.theme',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
    'session_security.middleware.SessionSecurityMiddleware',
    'flags.middleware.FlagConditionsMiddleware',
]


ROOT_URLCONF = 'urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJECT_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'builtins': [
                'base.templatetags.joplin_tags',
            ],
            'context_processors': [
                'base.context_processors.settings_context',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'wsgi.application'


# Detect whether it is a staging or production environment
DEPLOYMENT_MODE = os.environ.get('DEPLOYMENT_MODE', 'LOCAL')
IS_LOCAL = DEPLOYMENT_MODE == "LOCAL"
IS_PRODUCTION = DEPLOYMENT_MODE == "PRODUCTION"
IS_STAGING = DEPLOYMENT_MODE == "STAGING"
IS_REVIEW = DEPLOYMENT_MODE == "REVIEW"
IS_TEST = DEPLOYMENT_MODE == "TEST"


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases
#
# dj_database_url should detect the environment variable 'DATABASE_URL',
# this is provided by Heroku in production, or locally via Dockerfile.local,
# if it does not, then assume SQLite.
#
default_db_url = f'sqlite:///{os.path.join(PROJECT_DIR, "db.sqlite3")}'
DATABASES = {
    'default': dj_database_url.config(default=default_db_url, engine='django_postgrespool2', conn_max_age=0),
}

DATABASE_POOL_CLASS = 'sqlalchemy.pool.QueuePool'
# https://github.com/lcd1232/django-postgrespool2#configuration

# smaller pool to avoid going over connection limit
# related to gunicorn worker settings
safe_pool = {
    'max_overflow': 8,
    'pool_size': 4,
    'recycle': 200
}

# we can have more connections on the heroku standard db, so lets open the pool
# the formula is some combo of workers + worker_connections * pool_size + max_overflow
# this could be bigger but I also upped worker_connections in gunicorn.conf
bigger_pool = {
    'max_overflow': 10,
    'pool_size': 8,
    'recycle': 500
}

if IS_STAGING or IS_PRODUCTION:
    DATABASE_POOL_ARGS = safe_pool
else:
    DATABASE_POOL_ARGS = safe_pool

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

USE_I18N = True
USE_L10N = True

LANGUAGE_CODE = 'en-us'
SUPPORTED_LANGS = (
    'en',
    'es',
    'vi',
    'ar',
)
LANGUAGES = [lang for lang in global_settings.LANGUAGES if lang[0]
             in SUPPORTED_LANGS]

TIME_ZONE = 'UTC'
USE_TZ = True

MODELTRANSLATION_DEFAULT_LANGUAGE = 'en'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

STATICFILES_DIRS = [
    os.path.join(PROJECT_DIR, 'static'),
]

WEBPACK_LOADER = {
    'DEFAULT': {
        'BUNDLE_DIR_NAME': 'webpack_bundles/',
        'STATS_FILE': os.path.join(BASE_DIR, 'joplin/static/webpack-stats.json'),
    }
}

SMUGGLER_FIXTURE_DIR = os.path.join(BASE_DIR, 'joplin/db/smuggler')

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

WAGTAILDOCS_SERVE_METHOD = 'direct'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

CORS_ORIGIN_ALLOW_ALL = True
ALLOWED_HOSTS = [
    'localhost',
    '.herokuapp.com',
]

DEBUG_TOOLBAR = bool(strtobool(os.environ.get('DEBUG_TOOLBAR', str(False))))
MONITOR_PERFORMANCE = bool(strtobool(os.environ.get('MONITOR_PERFORMANCE', str(False))))

WAGTAILEMBEDS_RESPONSIVE_HTML = True

if MONITOR_PERFORMANCE:
    MIDDLEWARE.insert(1, 'silk.middleware.SilkyMiddleware')

    SILKY_PYTHON_PROFILER = False
    SILKY_PYTHON_PROFILER_BINARY = False
    SILKY_META = True
    SILKY_AUTHENTICATION = True
    SILKY_AUTHORISATION = True
    SILKY_MAX_RECORDED_REQUESTS = 10**3


if DEBUG_TOOLBAR:
    # TODO: only allow toolbar to be visible for admins
    def show_toolbar(request):
        return True

    DEBUG_TOOLBAR_CONFIG = {
        'SHOW_TOOLBAR_CALLBACK': show_toolbar,
    }

    INSTALLED_APPS = INSTALLED_APPS + [
        'debug_toolbar',
        'pympler'
    ]

    MIDDLEWARE.insert(1, 'debug_toolbar.middleware.DebugToolbarMiddleware')

    DEBUG_TOOLBAR_PANELS = [
        'debug_toolbar.panels.profiling.ProfilingPanel',
        'pympler.panels.MemoryPanel',
        'debug_toolbar.panels.versions.VersionsPanel',
        'debug_toolbar.panels.timer.TimerPanel',
        'debug_toolbar.panels.settings.SettingsPanel',
        'debug_toolbar.panels.headers.HeadersPanel',
        'debug_toolbar.panels.request.RequestPanel',
        'debug_toolbar.panels.sql.SQLPanel',
        'debug_toolbar.panels.templates.TemplatesPanel',
        'debug_toolbar.panels.staticfiles.StaticFilesPanel',
        'debug_toolbar.panels.cache.CachePanel',
        'debug_toolbar.panels.signals.SignalsPanel',
        'debug_toolbar.panels.logging.LoggingPanel',
        'debug_toolbar.panels.redirects.RedirectsPanel',
    ]


if DEBUG:
    ALLOWED_HOSTS.append('*')


# Wagtail settings
WAGTAIL_SITE_NAME = 'joplin'
WAGTAIL_AUTO_UPDATE_PREVIEW = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'fake_key')

# Email Settings
EMAIL_BACKEND = 'django_ses.SESBackend'
AWS_SES_REGION_NAME = 'us-east-1'
AWS_SES_REGION_ENDPOINT = 'email.us-east-1.amazonaws.com'
AWS_SES_ACCESS_KEY_ID = os.getenv('AWS_SES_ACCESS_KEY_ID', None)
AWS_SES_SECRET_ACCESS_KEY = os.getenv('AWS_SES_SECRET_ACCESS_KEY', None)
DEFAULT_FROM_EMAIL = os.getenv('EMAIL_HOST_USER', None)
WAGTAILADMIN_NOTIFICATION_FROM_EMAIL = os.getenv('EMAIL_HOST_USER', None)
WAGTAIL_EMAIL_MANAGEMENT_ENABLED = True
WAGTAIL_PASSWORD_MANAGEMENT_ENABLED = True
WAGTAIL_PASSWORD_RESET_ENABLED = True
WAGTAILUSERS_PASSWORD_ENABLED = False # Don't allow admins to edit passwords from the "Users" view

JANIS_URL = os.getenv('JANIS_URL', 'http://localhost:3000')


GRAPHENE = {
    'SCHEMA': 'api.schema.schema',
    'MIDDLEWARE': [
        'graphene_django.debug.DjangoDebugMiddleware',
        'graphql_jwt.middleware.JSONWebTokenMiddleware',
    ]
}

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'graphql_jwt.backends.JSONWebTokenBackend',
]

# Assume DB default settings for LOCAL env
DBBACKUP_STORAGE = 'django.core.files.storage.FileSystemStorage'
DBBACKUP_STORAGE_OPTIONS = {'location': '/app/joplin/db/backups'}


SMUGGLER_EXCLUDE_LIST = [
    'users.user'
]

# Avoid exporting owner settings
DBBACKUP_CONNECTORS = {
    'default': {
        'DUMP_SUFFIX': '--no-owner'
    }
}


#
# Production, Staging & Review Apps
#
if(IS_PRODUCTION or IS_STAGING or IS_REVIEW):
    #
    # AWS Buckets only if not local.
    #
    APPNAME = os.getenv('APPNAME')
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID', None)
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', None)
    AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_S3_BUCKET_STATIC')
    AWS_ARCHIVE_BUCKET_NAME = os.getenv('AWS_S3_BUCKET_ARCHIVE')
    AWS_BACKUPS_LOCATION = os.getenv('AWS_S3_BUCKET_ARCHIVE_LOCATION')
    AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

    #
    # Deployment Variables: AWS ECS Task Definition, CloudFront Distribution
    #
    AWS_ECS_DEPLOYMENT_BUCKET = os.getenv('AWS_ECS_DEPLOYMENT_BUCKET')
    AWS_ECS_TASK_DEFINITION = os.getenv('AWS_ECS_TASK_DEFINITION')
    AWS_CLOUDFRONT_DISTRIBUTION = os.getenv('AWS_CLOUDFRONT_DISTRIBUTION')

    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400',
    }

    # We now change the backups directory
    DBBACKUP_STORAGE_OPTIONS = {
        'access_key': AWS_ACCESS_KEY_ID,
        'secret_key': AWS_SECRET_ACCESS_KEY,
        'bucket_name': AWS_ARCHIVE_BUCKET_NAME,
        'host': "s3.amazonaws.com",
        'location': AWS_BACKUPS_LOCATION + "/" + APPNAME
    }

    # Specifying the location of files
    # The Janis CMS_MEDIA = 'https://' + AWS_S3_CUSTOM_DOMAIN + '/' + AWS_LOCATION
    if IS_PRODUCTION:
        AWS_LOCATION = 'production/static'
        AWS_IS_GZIPPED = True
        MEDIAFILES_LOCATION = 'production/media'
    elif IS_STAGING:
        AWS_LOCATION = 'staging/static'
        AWS_IS_GZIPPED = True
        MEDIAFILES_LOCATION = 'staging/media'
    else:
        AWS_LOCATION = f"review/{os.getenv('CIRCLE_BRANCH')}/static"
        AWS_IS_GZIPPED = True
        MEDIAFILES_LOCATION = f"review/{os.getenv('CIRCLE_BRANCH')}/media"

    # We now change the storage mode to S3 via Boto for default, static and dbbackup
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    """
    we could probably have media use this config as well to avoid the extra custom_storages.py
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    """
    DEFAULT_FILE_STORAGE = 'custom_storages.MediaStorage'
    DBBACKUP_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

JANIS_SLUG_URL = ""

if IS_PRODUCTION:
    JANIS_SLUG_URL = 'https://api.github.com/repos/cityofaustin/janis/tarball/production'

if IS_STAGING:
    JANIS_SLUG_URL = 'https://api.github.com/repos/cityofaustin/janis/tarball/master'

# security logout ward after half of expire value (four hours currently)
SESSION_SECURITY_WARN_AFTER = 14400 / 2
SESSION_SECURITY_EXPIRE_AFTER = 14400
# lets us run timeout while staying logged in with closed browser tab (for now)
SESSION_SECURITY_INSECURE = True

PHONENUMBER_DEFAULT_REGION = 'US'

PHONENUMBER_DB_FORMAT = "RFC3966"

FLAGS = {
    'SHOW_EXTRA_PANELS': [{'condition': 'boolean', 'value': True}],
    'INCREMENTAL BUILDS': [{'condition': 'boolean', 'value': False}]
}

# $JOPLIN_APP_HOST_PORT is set by scripts/serve-local.sh
JOPLIN_APP_HOST_PORT = os.getenv('JOPLIN_APP_HOST_PORT', 8000)
# The CMS_API endpoint of the current Django App for published Janis to use
if IS_LOCAL or IS_TEST:
    # Base URL to use when referring to full URLs within the Wagtail admin backend -
    # e.g. in notification emails. Don't include '/admin' or a trailing slash
    BASE_URL = f'http://127.0.0.1:{JOPLIN_APP_HOST_PORT}'
    CMS_API = f"{BASE_URL}/api/graphql"
    PREVIEW_CMS_API = f"{BASE_URL}/api/preview/graphql"
else:
    BASE_URL = f"https://{os.getenv('APPNAME','')}.herokuapp.com"
    CMS_API = f"{BASE_URL}/api/graphql"
    PREVIEW_CMS_API = f"{BASE_URL}/api/preview/graphql"


# Sets the login_url redirect for "from django.contrib.auth.decorators import user_passes_test"
# https://kite.com/python/docs/django.contrib.auth.decorators.user_passes_test
LOGIN_URL = '/admin/login/'

# https://docs.djangoproject.com/en/2.2/ref/settings/#data-upload-max-number-fields
# We submit a lot of fields when saving some of our content types, let's let that happen
DATA_UPLOAD_MAX_NUMBER_FIELDS = None
WAGTAILIMAGES_IMAGE_MODEL = 'base.TranslatedImage'

# Configs required to use SCOUT_APM
# SCOUT_MONITOR, SCOUT_KEY env vars are automatically provided by Heroku when you provision the addon
SCOUT_MONITOR = bool(strtobool(os.environ.get('SCOUT_MONITOR', str(False))))
if SCOUT_MONITOR:
    INSTALLED_APPS = [
        "scout_apm.django",
    ] + INSTALLED_APPS

    SCOUT_NAME = os.environ.get('APPNAME')


# Set configs for Janis Publisher_v2
PUBLISH_ENABLED = False
MOCK_PUBLISH = False
if IS_LOCAL:
    # Add mock "Publishing" status notifications when running locally.
    # Publishing does not work locally, the page will not actually be published.
    MOCK_PUBLISH = True
    API_PASSWORD = os.getenv("API_PASSWORD", 'x')
if IS_REVIEW:
    PUBLISHER_V2_URL = os.getenv("CI_COA_PUBLISHER_V2_URL_PR")
    PUBLISHER_V2_API_KEY = os.getenv("COA_PUBLISHER_V2_API_KEY_PR")
    PUBLISH_ENABLED = True
    API_PASSWORD = os.getenv("API_PASSWORD_REVIEW")
elif IS_STAGING:
    PUBLISHER_V2_URL = os.getenv("CI_COA_PUBLISHER_V2_URL_STAGING")
    PUBLISHER_V2_API_KEY = os.getenv("COA_PUBLISHER_V2_API_KEY_STAGING")
    PUBLISH_ENABLED = True
    API_PASSWORD = os.getenv("API_PASSWORD_STAGING")
elif IS_PRODUCTION:
    PUBLISHER_V2_URL = os.getenv("CI_COA_PUBLISHER_V2_URL_PROD")
    PUBLISHER_V2_API_KEY = os.getenv("COA_PUBLISHER_V2_API_KEY_PROD")
    PUBLISH_ENABLED = True
    API_PASSWORD = os.getenv("API_PASSWORD_PROD")
# For use with rest_framework_api_key
# Sets the name of the header required for Publisher to access publish_succeeded endpoint
# "Joplin-Api-Key": "********"
# https://florimondmanca.github.io/djangorestframework-api-key/guide/#custom-header
API_KEY_CUSTOM_HEADER = "HTTP_JOPLIN_API_KEY"


# Set logger level
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'joplin': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        },
    },
}

# Custom User Form Settings
AUTH_USER_MODEL = 'users.User'
WAGTAIL_USER_EDIT_FORM = 'users.forms.CustomUserEditForm'
WAGTAIL_USER_CREATION_FORM = 'users.forms.CustomUserCreationForm'

if IS_LOCAL or IS_TEST:
    # Allow non HTTPS requests when running a local Janis build from localhost.
    SECURE_SSL_REDIRECT = False
    SERVER_PROTOCOL = 'HTTP/0.9'
else:
    # Redirect to HTTPS
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
