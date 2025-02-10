import os
from pathlib import Path
from dotenv import load_dotenv

from .vendor.filebrowser import (
    FILEBROWSER_DIRECTORY,
    FILEBROWSER_VERSIONS,
    FILEBROWSER_EXTENSIONS,
    FILEBROWSER_ADMIN_VERSIONS,
    FILEBROWSER_ADMIN_THUMBNAIL,
    FILEBROWSER_MAX_UPLOAD_SIZE,
    FILEBROWSER_VERSION_QUALITY,
    VERSION_QUALITY,
    NORMALIZE_FILENAME,
    MAX_UPLOAD_SIZE,
    FILEBROWSER_SHOW_IN_DASHBOARD,
)

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_PATH = BASE_DIR / '../environment/secrets/.env'
load_dotenv(SECRET_PATH)

SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = int(os.environ.get('DEBUG', default=0))

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', default='').split()

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'filebrowser',

    'src.accounts.apps.AccountsConfig',
    'src.storage.apps.StorageConfig',
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

ROOT_URLCONF = 'config.urls'

HOST_SCHEME = os.environ.get('HOST_SCHEME')
PARENT_HOST = os.environ.get('PARENT_HOST')

SITE_TITLE = os.environ.get('SITE_TITLE')
SITE_HEADER = os.environ.get('SITE_HEADER')
INDEX_TITLE = os.environ.get('INDEX_TITLE')
SITE_URL = f'{HOST_SCHEME}{PARENT_HOST}'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'builtins': [
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

AUTH_USER_MODEL = 'accounts.User'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DB_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': os.environ.get('DB_NAME', BASE_DIR / '../environment/databases/db.sqlite3'),
        'USER': os.environ.get('DB_USER', 'user'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'password'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]


LANGUAGE_CODE = 'ru-RU'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_L10N = True
USE_TZ = True

DATE_FORMAT = 'j E Y'

STATIC_URL = os.environ.get('STATIC_URL', 'assets/')
STATIC_ROOT = BASE_DIR / os.environ.get('STATIC_ROOT', '../environment/public/assets')
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

MEDIA_URL = os.environ.get('MEDIA_URL', 'uploads/')
MEDIA_ROOT = BASE_DIR / os.environ.get('MEDIA_ROOT', '../environment/public/uploads')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CSRF_COOKIE_SECURE = int(os.environ.get('CSRF_COOKIE_SECURE', default=0))
SESSION_COOKIE_SECURE = int(os.environ.get('SESSION_COOKIE_SECURE', default=0))
SECURE_SSL_REDIRECT = int(os.environ.get('SECURE_SSL_REDIRECT', default=0))
