"""
Django settings for motheo_call_manager project.

Generated by 'django-admin startproject' using Django 3.0.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""
import configparser
import os
import sys
from django.core.management.color import color_style

style = color_style()


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

APP_NAME = 'motheo_call_manager'

LOGIN_REDIRECT_URL = 'home_url'

INDEX_PAGE = 'motheo.bhp.org.bw'

ETC_DIR = '/etc/motheo/'

CONFIG_FILE = f'{APP_NAME}.ini'

CONFIG_PATH = os.path.join(ETC_DIR, CONFIG_FILE)
sys.stdout.write(style.SUCCESS(f'  * Reading config from {CONFIG_FILE}\n'))

config = configparser.ConfigParser()
config.read(CONFIG_PATH)

SITE_ID = 1

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'gc2s5qt4g7(&scfo8xqra6wrn0%a!io4)g^yp@*nwa4e1hre7_'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# KEY_PATH = os.path.join(ETC_DIR, 'crypto_fields')

ALLOWED_HOSTS = ['localhost', 'motheo-test.bhp.org.bw', '127.0.0.1', '10.113.201.212']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django_crypto_fields.apps.AppConfig',
    'django_q',
    'crispy_forms',
    'rest_framework',
    'edc_call_manager.apps.AppConfig',
    'edc_dashboard.apps.AppConfig',
    'edc_device.apps.AppConfig',
    'edc_model_admin.apps.AppConfig',
    'edc_navbar.apps.AppConfig',
    'motheo_call_manager.apps.EdcBaseAppConfig',
    'motheo_call_manager.apps.EdcFacilityAppConfig',
    'motheo_call_manager.apps.EdcIdentifierAppConfig',
    'motheo_call_manager.apps.EdcProtocolAppConfig',
    'motheo_call_manager.apps.AppConfig',
    'django_extensions'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.sites.middleware.CurrentSiteMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'edc_dashboard.middleware.DashboardMiddleware',
    'edc_subject_dashboard.middleware.DashboardMiddleware',
]

ROOT_URLCONF = 'motheo_call_manager.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'motheo_call_manager.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

mysql_config = configparser.ConfigParser()
mysql_config.read(os.path.join(ETC_DIR, 'mysql.ini'))

HOST = mysql_config['mysql']['host']
DB_USER = mysql_config['mysql']['user']
DB_PASSWORD = mysql_config['mysql']['password']
DB_NAME = mysql_config['mysql']['database']
PORT = mysql_config['mysql']['port']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': HOST,   # Or an IP Address that your DB is hosted on
        'PORT': PORT,
    }
}

# Email configurations

EMAIL_BACKEND = config['email_conf'].get('email_backend')
EMAIL_HOST = config['email_conf'].get('email_host')
EMAIL_USE_TLS = config['email_conf'].get('email_use_tls')
EMAIL_PORT = config['email_conf'].get('email_port')
EMAIL_HOST_USER = config['email_conf'].get('email_user')
EMAIL_HOST_PASSWORD = config['email_conf'].get('email_host_pwd')

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

# REDCap API configurations

REDCAP_CONFIGURATION = {
    'OPTIONS': {
        'read_default_file': '/etc/motheo/redcap.conf',
    },
}

# Django q configurations

Q_CLUSTER = {
    'name': 'motheo_call_manager',
    'retry': 60,
    'timeout': 50,
    'orm': 'default',
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Gaborone'

USE_I18N = True

USE_L10N = False

USE_TZ = True

DASHBOARD_URL_NAMES = {}

DASHBOARD_BASE_TEMPLATES = {}

# Edc-facility
HOLIDAY_FILE = os.path.join(BASE_DIR, 'holidays.csv')
COUNTRY = 'botswana'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'motheo_call_manager', 'static')


if 'test' in sys.argv and 'mysql' not in DATABASES.get('default').get('ENGINE'):
    MIGRATION_MODULES = {
        "django_crypto_fields": None,
        "edc_call_manager": None,
        "edc_appointment": None,
        "edc_death_report": None,
        "edc_export": None,
        "edc_identifier": None,
        "edc_metadata": None,
        "edc_rule_groups": None,
        "edc_sync_files": None,
        "edc_sync": None,
        "motheo_call_manager": None}

if 'test' in sys.argv:
    PASSWORD_HASHERS = ('django_plainpasswordhasher.PlainPasswordHasher',)
    DEFAULT_FILE_STORAGE = 'inmemorystorage.InMemoryStorage'


DASHBOARD_URL_NAMES = {
    'call_manager_listboard_url': 'call_manager_listboard_url',

}

DASHBOARD_BASE_TEMPLATES = {
    'listboard_base_template': 'motheo_call_manager/base.html',
    'call_manager_listboard_template': 'motheo_call_manager/listboard.html',
}


REDCAP_API_URL = 'https://redcap-dev.bhp.org.bw/api/'
