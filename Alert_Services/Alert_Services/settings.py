"""
Django settings for Alert_Services project.

Using Django 1.8.4.
"""
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '-=+9px$u0-tch(bkyh4!-hkk22xpm$6s#ib&8zi8u=_kv51k)w'

DEBUG = True

ALLOWED_HOSTS = ['*']

# Celery settings
BROKER_URL = 'amqp://guest:guest@localhost//'
BROKER_POOL_LIMIT = 3
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_RESULT_BACKEND='amqp'
CELERY_TIMEZONE = 'America/New_York'
CELERY_ENABLE_UTC = True

#used for sslify
#SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'reddit_notifier',
)
INSTALLED_APPS += ('Alert_Services.celery.CeleryConfig', )

MIDDLEWARE_CLASSES = (
    #'sslify.middleware.SSLifyMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

# specifies root URL file
ROOT_URLCONF = 'Alert_Services.urls'

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

WSGI_APPLICATION = 'Alert_Services.wsgi.application'

# Database settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'PromptWorksDB',
        'USER': 'RyCSmith',
        'PASSWORD': 'amaSmitdb',
        'HOST': 'rcsdb.cjiemgsberaw.us-west-2.rds.amazonaws.com',
        'PORT': '3306',
    }
}

# Internationalization settings
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/New_York'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files settings (CSS, JavaScript, Images)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
