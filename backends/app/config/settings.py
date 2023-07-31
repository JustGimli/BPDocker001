"""
Django settings for app project.

Generated by 'django-admin startproject' using Django 4.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""


from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-c7+610)$6xd6(r&f*5925w^xnirad!d6k%up^o2^titrm2$$$('


DEBUG = bool(os.environ.get('DEBUG', default=False))

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True


if DEBUG:
    INTERNAL_IPS = ["127.0.0.1",]  # debug_toolbar

# ALLOWED_HOSTS = os.environ.get('ALLOWED_HOST', '127.0.0.1').split(' ')
# 185.59.216.0/24 (185.59.216.1 - 185.59.216.254)
ALLOWED_HOSTS = ['*']


INSTALLED_APPS = [
    'daphne',
    "corsheaders",
    # 'jet.dashboard',
    # 'jet',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'channels',
    # 'debug_toolbar',
    'rest_framework',
    'djoser',
    'django_celery_results',
    'apps.users.apps.UsersConfig',
    'apps.bots.apps.BotsConfig',
    'apps.chats.apps.ChatsConfig',
    'apps.projects.apps.ProjectsConfig',
    'apps.payments.apps.PaymentConfig',
    'apps.consultations.apps.ConsultationConfig',
    'apps.botusers.apps.BotusersConfig'
]


MIDDLEWARE = [

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    # 'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    # "config.middleware.SetRefreshTokenMiddleWare",
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

ASGI_APPLICATION = "config.asgi.application"
# WSGI_APPLICATION = 'config.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': os.environ.get('SQL_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': os.environ.get('SQL_DATABASE', 'db.sqlite3'),
        'USER': os.environ.get('SQL_USER'),
        'PASSWORD': os.environ.get('SQL_PASSWORD'),
        'HOST': os.environ.get('SQL_HOST'),
        'PORT': os.environ.get('SQL_PORT'),
    }
}


AUTH_USER_MODEL = "users.User"

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


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}


# REDIS
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'redis://' + os.environ.get('REDIS_HOST', '127.0.0.1') + ':6379/1',
    }
}


CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [(os.environ.get('REDIS_HOST', '127.0.0.1'), 6379)],
        },
    },
}


# CELERY

CELERY_CACHE_BACKEND = 'default'

CELERY_BROKER_URL = os.environ.get("BROKER_URL", "redis://localhost:6379/0")
CELERY_RESULT_BACKEND = os.environ.get(
    "RESULT_BACKEND", "redis://localhost:6379/0")

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

# LANGUAGES = (
#     ('en-us', 'English'),
#     ('ru', 'Russian'),
# )

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'UTC'

USE_I18N = True


USE_TZ = True


STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# LOCALE_PATHS = (os.path.join(BASE_DIR, 'locale'),)

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# JWT
SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('JWT',),
}


# djoser

DJOSER = {
    'SEND_ACTIVATION_EMAIL': True,
    'SET_PASSWORD_RETYPE': True,
    'ACTIVATION_URL': 'activate/{uid}/{token}/',
    'SERIALIZERS': {},
    "EMAIL": {
        "activation": "apps.users.email.ActivationEmail",
        'password_reset': 'apps.users.email.PasswordResetEmail',
    },
    "PASSWORD_RESET_CONFIRM_URL": "password-reset/{uid}/{token}",
    'HIDE_USERS': True,

}


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.mail.ru'
EMAIL_PORT = 2525
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST_USER = 'help@botpilot.ru'
EMAIL_HOST_PASSWORD = '4vusP41A2fNTdtgRC8bg'
DEFAULT_FROM_EMAIL = "БотПилот <help@botpilot.ru>"

# EMAIL_HOST_PASSWORD = 'gA?R2YIpuyh5'
