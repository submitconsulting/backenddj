# _*_ coding: utf-8 _*_
"""
Django settings for backenddj project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
#from os.path import normpath #abspath, basename, dirname, join, normpath
BASE_DIR = os.path.dirname(os.path.dirname((__file__)))
#BASE_DIR = BASE_DIR #.replace('\\', '/')
#print "mio %s" % (BASE_DIR)
#from sys import path
#path.append(BASE_DIR)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '#zqk3o8k!^3j)5g5r=rlt#xz@km+a7f5og$9(&_$69v@4^%4uh'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['*',]


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django.contrib.sites',
    
    'django.contrib.admindocs',
    
    'django.contrib.humanize',
    
    # Apss del mod Backend
    'apps.utils',
    'apps.params',
    'apps.space',
    'apps.sad',
    'apps.accounts',
    'apps.home',
    'apps.mod_backend',
    
    # Apss del mod ventas
    'apps.maestros',
    'apps.mod_ventas',
    
    # Apss del mod profesional
    'apps.rrhh',
    'apps.mod_pro',
    
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #'djangobb_forum.middleware.TimezoneMiddleware',
)

ROOT_URLCONF = 'backenddj.urls'

WSGI_APPLICATION = 'backenddj.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'es-pe' #en-us es-pe #valido también para datos enviado por javascript

TIME_ZONE = 'America/Lima' #'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

USE_THOUSAND_SEPARATOR = True

# Absolute path to the directory static files should be collected to.
if DEBUG:
    STATIC_ROOT = os.path.join(BASE_DIR, '/static')
else:
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')

#ADMIN_MEDIA_PREFIX = '/static/admin/'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

#
#
#
# Custom config

# Para mostrar la doc de la view http://localhost:8000/admin/doc/views/
SITE_ID = 1

# render to templates
TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_DIR, 'templates'),
)

#Backup/restore database https://code.djangoproject.com/wiki/Fixtures
FIXTURE_DIRS = (
    os.path.join(BASE_DIR, 'fixtures'),
)

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_DIR, 'static'),  # para cargar los js y css y tambien para {% load staticfiles %}
    #'./static/',
)

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

#'str' object has no attribute 'session' para la sessiones de Message
########## TEMPLATE CONFIGURATION #para session.get('flash_msg', False)
# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    # 'django.core.context_processors.l10n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
)
# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
   #  'django.template.loaders.eggs.Loader',
)

########## EXPIRE SESSION BROWSER CLOSE
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
########## END EXPIRE SESSION

#Locale, para cambiar de idioma
LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

########## MEDIA CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = '/media/'
# ADMIN_MEDIA_PREFIX="/media/admin/"
########## END MEDIA CONFIGURATION


########## CACHE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#caches  https://pythonhosted.org/johnny-cache/
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        # 'LOCATION': '127.0.0.1:11211',
        #'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
    }
}
########## END CACHE CONFIGURATION


#add email settings
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'asullom@gmail.com'
EMAIL_HOST_PASSWORD = '123xxxxx'
DEFAULT_FROM_EMAIL = 'asullom@gmail.com'

###########
# LOGGING #
###########
xxx = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'temp/logs/debug.log'),
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '[%(asctime)s][%(levelname)s] [%(name)s] %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'null': {
            'level':'DEBUG',
            'class':'django.utils.log.NullHandler',
        },
        'file_audit': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'simple',
            'filename': os.path.join(BASE_DIR, 'temp/logs','audit.log'),
            
        },
        'file_log': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'simple',
            'filename': os.path.join(BASE_DIR, 'temp/logs','log.log'),
            
        },
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        # I always add this handler to facilitate separating loggings
        #'log_file':{
        #    'level': 'DEBUG',
        #    'class': 'logging.handlers.RotatingFileHandler',
        #    'filename': os.path.join(BASE_DIR, 'temp/logs/log_file.log'),
        #    'maxBytes': '16777216', # 16megabytes
        #    'formatter': 'verbose'
        #},
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        }
    },
    'loggers': {
        'audit': {              # define a logger - give it a name
            'handlers': ['file_audit'], # specify what handler to associate
            'level': 'INFO',                 # specify the logging level
            'propagate': True,
        },
        'log': {              # define a logger - give it a name
            'handlers': ['file_log'], # specify what handler to associate
            'level': 'INFO',                 # specify the logging level
            'propagate': True,
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        #'apps': { # I keep all my of apps under 'apps' folder, but you can also add them one by one, and this depends on how your virtualenv/paths are set
        #    'handlers': ['log_file'],
        #    'level': 'INFO',
        #    'propagate': True,
        #},
    },
    # you can also shortcut 'loggers' and just configure logging for EVERYTHING at once
    'root': {
        'handlers': ['console', 'mail_admins'],
        'level': 'INFO'
    },
}

