"""
Django settings for HyperAnnales project.

Generated by 'django-admin startproject' using Django 3.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

from dotenv import load_dotenv
import os


# Import environment files
env_path = "/home/secret/password.env"
load_dotenv(dotenv_path=env_path)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    'dev.annales.hyperion.tf',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
}

# Application definition

INSTALLED_APPS = [
    # My apps
    'accounts',
    'static_files',

    # Django REST
    'rest_framework',

    # Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_sendfile',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'HyperAnnales.urls'

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
            'debug': DEBUG
        },
    },
]

AUTH_USER_MODEL = 'accounts.Account'

WSGI_APPLICATION = 'HyperAnnales.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DEFAULT_DB_ALIAS = 'user_ref'

DATABASES = {
    'default': {},
    'user_ref': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv("USER_NAME"),
        'USER': os.getenv("USER_USER"),
        'PASSWORD': os.getenv("USER_PASS"),
        'HOST': os.getenv("USER_HOST"),
        'PORT': int(os.getenv("USER_PORT")),
    },
    'pdf_ref': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv("PDF_NAME"),
        'USER': os.getenv("PDF_USER"),
        'PASSWORD': os.getenv("PDF_PASS"),
        'HOST': os.getenv("PDF_HOST"),
        'PORT': int(os.getenv("PDF_PORT")),
    }
}


DATABASE_ROUTERS = ['HyperAnnales.routers.HyperionRouter']


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

# Cache system

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/tmp/HyperAnnales_cache',
    }
}


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Email settings

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = os.getenv("EMAIL_HOST_OVH")

EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER_OVH")

EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASS_OVH")

EMAIL_PORT = os.getenv("EMAIL_PORT_OVH")

EMAIL_USE_SSL = bool(int(os.getenv("EMAIL_SSL_OVH")))

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = "/static/"

MEDIA_ROOT = "/media/static_HA/"

# STATIC_ROOT = "/home/static_HA/"

# Configuration to sendfile package

SENDFILE_BACKEND = "django_sendfile.backends.simple"

KEY_TOKEN = os.getenv("PRIVATE_TOKEN")

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# Unsecured media files

BASE_MEDIA_URL = "https://raw.githubusercontent.com/Hyperion60/"
BASE_MEDIA_ROOT = "/media/media_HA/"