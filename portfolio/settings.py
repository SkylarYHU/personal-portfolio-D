import dj_database_url
import os
from pathlib import Path
from os import getenv
import socket
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Check if we're in production (Heroku sets this)
IS_DEVELOPMENT_VAR = os.getenv('IS_DEVELOPMENT', 'True')
IS_PRODUCTION = IS_DEVELOPMENT_VAR.lower() == 'false'
print(f"[SETTINGS] IS_DEVELOPMENT env var: {IS_DEVELOPMENT_VAR}, IS_PRODUCTION: {IS_PRODUCTION}")

# Only load .env file in local development
if not IS_PRODUCTION:
    load_dotenv()

# SECURITY WARNING: keep the secret key used in production secret!
# This should be set in your environment variables, not generated here
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-insecure-local-dev-key-change-in-production-123456789')

# SECURITY WARNING: don't run with debug turned on in production!
# In production, IS_DEVELOPMENT should be explicitly set to False
DEBUG = os.getenv("IS_DEVELOPMENT", "True").lower() == "true" and not IS_PRODUCTION

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

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', default_hosts).split(',')
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
    "storages",
    "adminsortable2",
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

# File Upload Settings
# 限制文件上传大小，防止内存溢出和超时
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB
DATA_UPLOAD_MAX_NUMBER_FIELDS = 1000

# Request timeout settings
# 防止长时间请求导致超时
if IS_PRODUCTION:
    # 生产环境使用较短的超时时间
    CONN_MAX_AGE = 60
    DATABASES['default']['CONN_MAX_AGE'] = CONN_MAX_AGE

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

# AWS S3 Configuration
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME', 'us-east-1')
AWS_S3_CUSTOM_DOMAIN = os.getenv('AWS_S3_CUSTOM_DOMAIN')
AWS_CLOUDFRONT_DOMAIN = os.getenv('AWS_CLOUDFRONT_DOMAIN')  # CloudFront CDN域名
AWS_DEFAULT_ACL = None  # 不设置ACL，因为存储桶不允许ACL
AWS_QUERYSTRING_AUTH = False  # 不使用查询字符串认证，允许公共访问
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=31536000',  # 1年缓存
    'Expires': 'Thu, 31 Dec 2099 20:00:00 GMT',
}

# 添加文件类型映射，确保图片文件有正确的 Content-Type
AWS_S3_FILE_OVERWRITE = False  # 避免覆盖同名文件
AWS_S3_SIGNATURE_VERSION = 's3v4'  # 使用签名版本4

# 自定义存储类来设置正确的 Content-Type
from storages.backends.s3boto3 import S3Boto3Storage

class MediaStorage(S3Boto3Storage):
    bucket_name = AWS_STORAGE_BUCKET_NAME
    custom_domain = AWS_CLOUDFRONT_DOMAIN or AWS_S3_CUSTOM_DOMAIN  # 优先使用CloudFront
    default_acl = None  # 不设置ACL，因为存储桶不允许ACL
    querystring_auth = False
    
    def _save(self, name, content):
        # 根据文件扩展名设置正确的 Content-Type
        import mimetypes
        content_type, _ = mimetypes.guess_type(name)
        if content_type:
            content.content_type = content_type
        return super()._save(name, content)

# Production settings - force S3 usage when in production
if IS_PRODUCTION or not DEBUG:
    # Use S3 for media files in production
    if AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY and AWS_STORAGE_BUCKET_NAME and (AWS_CLOUDFRONT_DOMAIN or AWS_S3_CUSTOM_DOMAIN):
        DEFAULT_FILE_STORAGE = 'portfolio.settings.MediaStorage'
        domain = AWS_CLOUDFRONT_DOMAIN or AWS_S3_CUSTOM_DOMAIN
        MEDIA_URL = f'https://{domain}/'
        if AWS_CLOUDFRONT_DOMAIN:
            print(f"[SETTINGS] Using CloudFront CDN: {MEDIA_URL}")
        else:
            print(f"[SETTINGS] Using S3 storage: {MEDIA_URL}")
    else:
        print(f"[SETTINGS] Missing AWS config - AWS_ACCESS_KEY_ID: {bool(AWS_ACCESS_KEY_ID)}, AWS_SECRET_ACCESS_KEY: {bool(AWS_SECRET_ACCESS_KEY)}, AWS_STORAGE_BUCKET_NAME: {AWS_STORAGE_BUCKET_NAME}, AWS_S3_CUSTOM_DOMAIN: {AWS_S3_CUSTOM_DOMAIN}")
        # Fallback to local media serving
        STATICFILES_DIRS.append(os.path.join(BASE_DIR, 'media'))
else:
    print(f"[SETTINGS] Development mode - using local storage")
    
    # Keep WhiteNoise for static files
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
    WHITENOISE_USE_FINDERS = True
    WHITENOISE_AUTOREFRESH = True

# Logging configuration for better error tracking
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}
