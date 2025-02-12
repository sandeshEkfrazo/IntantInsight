"""
Django settings for robas project.

Generated by 'django-admin startproject' using Django 3.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
from datetime import timedelta
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-#r$4&mw@h+(svs^bopg^*hni5)nvgnk-skn1@o*@sdc6#f+^!b+robas'
ENCRYPTED_ID = "insantInsightEnc"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

#URL
LIVE_URL = "https://instantinsightz.com"
# LIVE_URL = "https://robas.thestorywallcafe.com"

ALLOWED_HOSTS = ["143.110.185.59", "localhost:4200", '*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'account',
    'projects',
    'prescreener',
    'sampling',
    'panelbuilding',
    'panelengagement',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'rest_framework_swagger',
    'drf_yasg',
    'rest_framework_simplejwt',
    'django_filters',
    'celery',
    'django_celery_results',
    'django_celery_beat',
    'import_export',
    'surveyQuestionare',
    'comman',
    'masters',
    'usersurvey',
    'django_user_agents',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_user_agents.middleware.UserAgentMiddleware',
]

ROOT_URLCONF = 'robas.urls'

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

WSGI_APPLICATION = 'robas.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'read_default_file': '/instantInsight/auth/mysql.cnf',
        },
    }
}


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'robas',
#         'USER':'root',
#         'PASSWORD':'',
#         'HOST':'127.0.0.1',
#         'PORT':'3307',
#     }
# }



# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

MEDIA_URL = '/media/'

# STATIC_ROOT = os.path.join(BASE_DIR,'static')
# MEDIA_ROOT = os.path.join(BASE_DIR,'media')



# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_USE_TLS = True
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_HOST_USER = 'gunjan.kr518@gmail.com'
# EMAIL_HOST_PASSWORD = 'aeiousharma@#@#'
# EMAIL_PORT = 587

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'donotreplyrobas@gmail.com'
EMAIL_HOST_PASSWORD = 'ugkcwzivtlojlpai'
# EMAIL_HOST_USER = 'research@buzz-thepanel.com'
# EMAIL_HOST_PASSWORD = 'Robas@12#'
EMAIL_PORT = 587
APPLICATION_EMAIL = 'Robas<donotreplyrobas@gmail.com>'
DEFAULT_FROM_EMAIL = 'Robas<donotreplyrobas@gmail.com>'



# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=10),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=2),


    'AUTH_HEADER_TYPES': ('Bearer',),

}
#REST_FRAMEWORK = {
#
#  'DEFAULT_AUTHENTICATION_CLASSES': (
#
#        'rest_framework_simplejwt.authentication.JWTAuthentication',
#   ),


    
    
#}
#JWT
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
# JWT_SECRET_KEY = 'wcwef*rax1mz3gr$f&)gzo@bdbx)rml19ykmz+51*tj!j_yyp-'
CORS_ORIGIN_ALLOW_ALL   = True
CORS_ALLOW_CREDENTIALS  = True


JWT = {
    'JWT_SECRET': os.getenv('JWT_SECRET_KEY'),
    # 'JWT_EXP_DELTA_DAYS':'5'
}

# CELERY_BROKER_URL = "127.0.0.1:6379"
# CELERY_RESULT_BACKEND = "127.0.0.1:6379"
# CELERY_ACCEPT_CONTENT = ['application/json']
# CELERY_RESULT_SERIALIZER = 'json'
# CELERY_TASK_SERIALIZER = 'json'

CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379'
CELERY_BROKER_URL = 'redis://127.0.0.1:6379'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Kolkata'
CELERY_ACCEPT_CONTENT = ['application/json']

# IMPORT_EXPORT_USE_TRANSACTIONS = True
STATIC_ROOT="/instantInsight/site/public/static"
MEDIA_ROOT="instantInsight/site/public/media"

STATICFILES_DIRS = [
        '/instantInsight/site/public/static/frontend/dist'
]  
