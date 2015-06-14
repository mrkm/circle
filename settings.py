# -*- coding: utf-8 -*-
import sys
import os
import secret
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "libs"))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "apps"))
DEBUG = os.environ.get('SERVER_SOFTWARE', '').startswith('Development')
TEMPLATE_DEBUG = DEBUG
ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
    ('mrkm', 'mrkm978+circle@gmail.com'),
)
EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'
TIME_ZONE = 'Asia/Tokyo'
LANGUAGE_CODE = 'ja'
SITE_ID = 1
USE_I18N = True
SECRET_KEY = secret.SECRET_KEY
ROOT_URLCONF = 'urls'
CONTACT_EMAIL = 'mrkm978+circle@gmail.com'
SITE_NAME = u"circle"
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)
TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, "templates"),
)
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
)
INSTALLED_APPS = (
    #'djangoappengine',
    #'djangotoolbox',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'core',
    'booking',
)
ALLOWED_HOSTS=['band9u.appspot.com']
