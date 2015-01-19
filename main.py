# pylint: disable=C0103
from __future__ import absolute_import
from django.core.handlers.wsgi import WSGIHandler
from django.conf import settings

def _setup_apps():
	from django.utils.importlib import import_module

	for _app in settings.INSTALLED_APPS:
		try:
			import_module('%s.models' % _app)
		except ImportError:
			pass

_setup_apps()

app = WSGIHandler()
