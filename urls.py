from django.conf.urls import patterns, url, include


urlpatterns = patterns('',
    (r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': '/media/images/favicon.ico'}),
    url(r'', include('core.urls')),
)
