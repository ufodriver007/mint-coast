"""
Django settings for mint_coast project.

Generated by 'django-admin startproject' using Django 4.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from dotenv import load_dotenv
from pathlib import Path


load_dotenv()

with open('blacklist.txt', 'r') as f:
    BLACKLIST = {item.strip(): '' for item in f}

DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DJANGO_SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
MAILRU_HOST_USER = os.getenv('MAILRU_HOST_USER')
MAILRU_HOST_PASSWORD = os.getenv('MAILRU_HOST_PASSWORD')
SOCIALACCOUNT_GIT_CLIENT_ID = os.getenv('SOCIALACCOUNT_GIT_CLIENT_ID')
SOCIALACCOUNT_GIT_SECRET_KEY = os.getenv('SOCIALACCOUNT_GIT_SECRET_KEY')
SOCIALACCOUNT_VK_CLIENT_ID = os.getenv('SOCIALACCOUNT_VK_CLIENT_ID')
SOCIALACCOUNT_VK_SECRET_KEY = os.getenv('SOCIALACCOUNT_VK_SECRET_KEY')
SOCIALACCOUNT_GOOGLE_CLIENT_ID = os.getenv('SOCIALACCOUNT_GOOGLE_CLIENT_ID')
SOCIALACCOUNT_GOOGLE_SECRET_KEY = os.getenv('SOCIALACCOUNT_GOOGLE_SECRET_KEY')
MY_RECAPTCHA_PUBLIC_KEY = os.getenv('MY_RECAPTCHA_PUBLIC_KEY')
MY_RECAPTCHA_PRIVATE_KEY = os.getenv('MY_RECAPTCHA_PRIVATE_KEY')
MY_DEFAULT_FROM_EMAIL = os.getenv('MY_DEFAULT_FROM_EMAIL')
MY_STATIC_ROOT = os.getenv('MY_STATIC_ROOT')


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = DJANGO_SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.mail.ru'
EMAIL_PORT = 2525
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST_USER = MAILRU_HOST_USER
EMAIL_HOST_PASSWORD = MAILRU_HOST_PASSWORD
DEFAULT_FROM_EMAIL = MY_DEFAULT_FROM_EMAIL

ALLOWED_HOSTS = ['mint-coast.ru', 'www.mint-coast.ru', '89.23.110.30', 'localhost', '127.0.0.1']


# Application definition
SITE_ID = 1

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django.contrib.postgres',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'mint_app',
    'mint_coast',
    'cart',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.github',
    'allauth.socialaccount.providers.vk',
    'allauth.socialaccount.providers.google',
    'rest_framework',
    'snowpenguin.django.recaptcha3',
    'debug_toolbar',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "allauth.account.middleware.AccountMiddleware",
    'mint_app.middleware.BanMiddleware',
    'mint_app.middleware.ThrottlingMiddleware',
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

ROOT_URLCONF = 'mint_coast.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'mint_app.context_processors.categories_proc',
            ],
        },
    },
]

WSGI_APPLICATION = 'mint_coast.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASS,
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATIC_URL = '/static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field


ACCOUNT_AUTHENTICATION_METHOD = 'email'      # Метод аутентификации - по электронной почте
ACCOUNT_EMAIL_REQUIRED = True                # Требовать адрес электронной почты при регистрации

AUTHENTICATION_BACKENDS = (
    'allauth.account.auth_backends.AuthenticationBackend',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIALACCOUNT_PROVIDERS = {
    'github': {
        "VERIFIED_EMAIL": True,
        'SCOPE': [
            'user',
            'repo',
            'read:org',
        ],
        'client_id': SOCIALACCOUNT_GIT_CLIENT_ID,
        'secret': SOCIALACCOUNT_GIT_SECRET_KEY,
        'key': '',
    },
    'vk': {
        'SCOPE': [
            'email',
            'first_name',
            'last_name',
        ],
        'client_id': SOCIALACCOUNT_VK_CLIENT_ID,
        'secret': SOCIALACCOUNT_VK_SECRET_KEY,
        'key': '',
    },
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
        'OAUTH_PKCE_ENABLED': True,
        'client_id': SOCIALACCOUNT_GOOGLE_CLIENT_ID,
        'secret': SOCIALACCOUNT_GOOGLE_SECRET_KEY,
        'key': '',
    },
}

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
    ),
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.UserRateThrottle',
        'rest_framework.throttling.AnonRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'user': '100/minute',  # Лимит для UserRateThrottle
        'anon': '10/minute',  # Лимит для AnonRateThrottle
    }
}

RECAPTCHA_PUBLIC_KEY = MY_RECAPTCHA_PUBLIC_KEY
RECAPTCHA_PRIVATE_KEY = MY_RECAPTCHA_PRIVATE_KEY
RECAPTCHA_DEFAULT_ACTION = "generic"
RECAPTCHA_SCORE_THRESHOLD = 0.5

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "site_log.log"),
            'formatter': 'simple',
        },
        "admin_file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "site_access_log.log"),
            'formatter': 'simple',
        },
    },
    "loggers": {
        "my_views": {
            "handlers": ["file"],
            "level": os.getenv("DJANGO_LOG_LEVEL", "DEBUG"),
            "propagate": False,
        },
        "admin": {
            "handlers": ["admin_file"],
            "level": os.getenv("DJANGO_LOG_LEVEL", "DEBUG"),
            "propagate": False,
        },
        "my_middleware": {
            "handlers": ["file"],
            "level": os.getenv("WARNING"),
            "propagate": False,
        },
    },
    'formatters': {
        'simple': {
            'format': '{asctime} - {levelname} - {name} - {message}',
            'style': '{'
        }
    },
}

INTERNAL_IPS = [
    "127.0.0.1",
]
