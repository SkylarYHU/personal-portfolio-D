import dj_database_url
import os
from pathlib import Path
from os import getenv
import socket

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
# This should be set in your environment variables, not generated here
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = getenv("IS_DEVELOPMENT", "True").lower() == "true"

# Allowed hosts should be set via environment variables, fallback to local and specific domain.
default_hosts = 'skylarhu.atwebpages.com,13.60.173.208,127.0.0.1,.herokuapp.com,skylarhu.work,www.skylarhu.work'

# Get the Heroku app name from environment variable
heroku_app_name = os.getenv('HEROKU_APP_NAME', '')
if heroku_app_name:
    default_hosts += f',{heroku_app_name}.herokuapp.com'

# 获取当前主机名和IP地址，用于解决IP不匹配问题
current_hostname = socket.gethostname()

# 尝试获取当前主机的IP地址
try:
    current_ip = socket.gethostbyname(current_hostname)
except:
    current_ip = ''

# 获取Heroku的动态IP地址
heroku_host = os.getenv('HEROKU_HOST', '')

ALLOWED_HOSTS = getenv('ALLOWED_HOSTS', default_hosts).split(',')
ALLOWED_HOSTS.append(current_hostname)
if current_ip:
    ALLOWED_HOSTS.append(current_ip)
if heroku_host:
    ALLOWED_HOSTS.append(heroku_host)

# 添加通配符，接受所有请求（仅在开发环境中使用）
if DEBUG:
    ALLOWED_HOSTS.append('*')

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "portfolioapp",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "portfolio.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "portfolio.wsgi.application"

# Database
DATABASES = {
    'default': {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

if not DEBUG:
    DATABASES['default'] = dj_database_url.config(
        conn_max_age=600, ssl_require=True)

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

if not DEBUG:
    # Production settings for static file serving with whitenoise
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
