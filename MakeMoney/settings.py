# Django settings for webapps project.

import os

import dj_database_url

# Sets the project path as a variable to be used below
BASE_DIR = os.path.realpath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__)) + '/'
APP_ROOT = os.path.abspath(os.path.join(PROJECT_ROOT, '..', 'beta/'))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Aayush Agarwal', 'aayusha@andrew.cmu.edu'),
    ('TK Abdul', 'tabdul@andrew.cmu.edu'),
)

MANAGERS = ADMINS

isLive = os.environ.get("DATABASE_URL") != None
 
if isLive:
    DATABASES = {'default': dj_database_url.config(default='postgres://localhost')}
else:
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': PROJECT_ROOT + 'db/webapps.db',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': '',
        'PASSWORD': '',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
        }
    }
LOGIN_URL = '/signin'
LOGIN_REDIRECT_URL = '/' # Do we need this? I called it home.html
AUTH_PROFILE_MODULE = 'beta.UserProfile'
ALLOWED_HOSTS = []
TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True
# Absolute filesystem path to the directory that will hold user-uploaded files.
MEDIA_ROOT = APP_ROOT + '/media/'

# URL that handles the media served from MEDIA_ROOT. 
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
STATIC_ROOT = os.path.join(PROJECT_ROOT,'static/')

# URL prefix for static files.
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'beta/static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '1fw$u=*8^#8!@m9!ws18$fjl(v7vhth^vk22idz+!afko%$^*='

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
)

# Configures Django to merely print emails rather than sending them.
# Comment out this line to enable real email-sending.
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# To enable real email-sending, you should uncomment and 
# configure the settings below.
# EMAIL_HOST = 'Your-SMTP-host'               # perhaps 'smtp.andrew.cmu.edu'
# EMAIL_HOST_USER = 'Your-SMTP-username'      # perhaps your Andrew ID
# EMAIL_HOST_PASSWORD = 'Your-SMTP-password'
# EMAIL_USE_TLS = True

ROOT_URLCONF = 'MakeMoney.urls'
WSGI_APPLICATION = 'MakeMoney.wsgi.application'
TEMPLATE_DIRS = '/beta/templates/'
INSTALLED_APPS = ('django.contrib.auth', 'django.contrib.contenttypes', 'django.contrib.sessions', 'django.contrib.sites', 'django.contrib.messages', 'django.contrib.staticfiles', 'django.contrib.admin', 'beta')
LOGGING = {'version': 1,
 'disable_existing_loggers': False,
 'filters': {'require_debug_false': {'()': 'django.utils.log.RequireDebugFalse'}},
 'handlers': {'mail_admins': {'level': 'ERROR',
                              'filters': ['require_debug_false'],
                              'class': 'django.utils.log.AdminEmailHandler'}},
 'loggers': {'django.request': {'handlers': ['mail_admins'],
                                'level': 'ERROR',
                                'propagate': True}}}

from django.core.exceptions import ImproperlyConfigured

def get_env_variable(var_name):
    """ Get the environment variable or return exception """
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = "Set the %s environment variable" % var_name
        raise ImproperlyConfigured(error_msg)


DEBUG = get_env_variable("DJANGO_DEBUG")
if DEBUG == 1 or DEBUG == '1':
    DEBUG = True
else:
    DEBUG = False
    
LOCAL_DEV = get_env_variable("DJANGO_LOCAL_DEV")
if LOCAL_DEV == 1 or LOCAL_DEV == '1':
    LOCAL_DEV = True
else:
    LOCAL_DEV = False

DATABASES = {}

if LOCAL_DEV:
    ALLOWED_HOSTS = ['*'] #useful when testing with DEBUG = FALSE
    INTERNAL_IPS = ('127.0.0.1',) #sets local IPS needed for DEBUG_TOOLBAR and other items.

    DATABASES = {
        'default': {
            
            'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
            #'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'MakeMoney',                      # Or path to database file if using sqlite3.
            #'NAME': '/Users/SomeUser/Documents/Django Projects/hellodjango/hellodjango.sql',                      # Or path to database file if using sqlite3.
            # The following settings are not used with sqlite3:
            'USER': '',
            'PASSWORD': '',
            'HOST': 'localhost',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
            'PORT': '',                      # Set to empty string for default.
        }
    }
else:
    # Parse database configuration from $DATABASE_URL
    DATABASES['default'] =  dj_database_url.config()
    
    # Honor the 'X-Forwarded-Proto' header for request.is_secure()
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

DEFAULT_FROM_EMAIL = get_env_variable("DJANGO_EMAIL_DEFAULT_USER")

SECRET_KEY = get_env_variable("DJANGO_SECRET_KEY")


