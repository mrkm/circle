# -*- coding: utf-8 -*-
import sys
import os

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "libs"))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "apps"))
DEBUG = os.environ.get('SERVER_SOFTWARE', '').startswith('Development')
TEMPLATE_DEBUG = DEBUG
ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
    ('mrkm', 'mrkm978+circle@gmail.com'),
)
TIME_ZONE = 'Asia/Tokyo'
LANGUAGE_CODE = 'ja'
SITE_ID = 1
USE_I18N = True
SECRET_KEY = 'u*@1b%2uv_%8yer15i38qxhvrs12z+e#103kx8)-jjq(cs#pm&'
ROOT_URLCONF = 'urls'
CONTACT_EMAIL = 'mrkm978+circle@gmail.com'
SITE_NAME = u"circle"
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
)
TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, "templates"),
)
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
)
INSTALLED_APPS = (
    'django.contrib.sessions',
    'core',
    'booking',
)
