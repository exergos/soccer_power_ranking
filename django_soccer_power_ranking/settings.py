"""
Django settings for django_soccer_power_ranking project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '-(b79id^=!!x&!7x6ld3798+e5r6ny60o$_6lg3^i9q&)x+&8)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


if DEBUG:
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/1.7/howto/static-files/
    STATIC_PATH = os.path.join(BASE_DIR, 'static')

    # Define STATIC_ROOT for apps that compress all static files into 1
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')

    STATIC_URL = '/static/'

    STATICFILES_DIRS = [
        STATIC_PATH,
        ]

    TEMPLATE_PATH = os.path.join(BASE_DIR, 'templates')

    TEMPLATE_DIRS = [
        TEMPLATE_PATH,
        ]
    # Database
    # https://docs.djangoproject.com/en/1.7/ref/settings/#databases

    # DATABASES = {
    #     'default': {
    #         'NAME': 'soccer_power_ranking',
    #         'ENGINE': 'mysql.connector.django',
    #         'USER': 'root',
    #         'PASSWORD': 'Will0870',
    #         'HOST': 'EXERGOS-PC',
    #         'OPTIONS': {
    #           'autocommit': True,
    #         },
    #     }
    # }

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'dctmfgvdrdled0',
            'USER': 'orlmfrokadzras',
            'PASSWORD': 'XZS2N1h6D-jDyNAbuRUpg1Uk8g',
            'HOST': 'ec2-54-228-227-13.eu-west-1.compute.amazonaws.com'
        }
    }

    STATICFILES_FINDERS = (
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    )

    ALLOWED_HOSTS = []

else:
    # HEROKU PRODUCTION
    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/1.7/howto/static-files/

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    # If collectstatic is used when uploading to heroku, use staticfiles root
    STATIC_ROOT = 'staticfiles'
    STATIC_URL = '/static/'

    STATICFILES_DIRS = (
        os.path.join(os.path.dirname(BASE_DIR), 'static'),
    )
    # Simplified static file serving.
    # https://warehouse.python.org/project/whitenoise/

    STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

    TEMPLATE_PATH = os.path.join(os.path.dirname(BASE_DIR), 'templates')

    TEMPLATE_DIRS = [
        TEMPLATE_PATH,
        ]

    # Production database

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'dctmfgvdrdled0',
            'USER': 'orlmfrokadzras',
            'PASSWORD': 'XZS2N1h6D-jDyNAbuRUpg1Uk8g',
            'HOST': 'ec2-54-228-227-13.eu-west-1.compute.amazonaws.com'
        }
    }

    STATICFILES_FINDERS = (
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    )

    # Allow all host headers
    ALLOWED_HOSTS = ['*']




TEMPLATE_DEBUG = True


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app_soccer_power_ranking',

    # gunicorn, for heroku deployment
    # "gunicorn",
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'django_soccer_power_ranking.urls'

WSGI_APPLICATION = 'django_soccer_power_ranking.wsgi.application'


# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True
