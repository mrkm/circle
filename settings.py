# -*- coding: utf-8 -*-
import sys
import os

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "libs"))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "apps"))
DEBUG = True
#DEBUG = False
TEMPLATE_DEBUG = DEBUG

# tells Pinax to use the default theme
PINAX_THEME = 'default'

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
    ('mrkm', 'mrkm978+circle@gmail.com'),
)

EMAIL_HOST = 'gmail.com'
DEFAULT_FROM_EMAIL = 'mrkm978+circle@gmail.com'
SERVER_EMAIL = 'mrkm978+circle@gmail.com'
EMAIL_PORT = "25"
EMAIL_SUBJECT_PREFIX = '[circle]'
EMAIL_USE_TLS = True
EMAIL_CONFIRMATION_DAYS = 2
EMAIL_DEBUG = DEBUG
MANAGERS = ADMINS
SEND_BROKEN_LINK_EMAILS = True

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Asia/Tokyo'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'ja'
SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

STATIC_URL = '/site_media/static/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
#ADMIN_MEDIA_PREFIX = '/media/'
ADMIN_MEDIA_PREFIX = '/site_media/static/admin/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'u*@1b%2uv_%8yer15i38qxhvrs12z+e#103kx8)-jjq(cs#pm&'

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, "templates"),
    #os.path.join(PINAX_ROOT, "templates", PINAX_THEME),
)
CONTACT_EMAIL = 'mrkm978+circle@gmail.com'
SITE_NAME = u"circle"

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
)


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'core',
    'booking',
)
