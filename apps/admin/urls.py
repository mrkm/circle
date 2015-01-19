from django.conf.urls import patterns, url
from core.views import TopView, DeleteView


urlpatterns = patterns('',
    url(r'^$', TopView.as_view(), name='home'),
    url(r'^delete/(?P<pk>\d+)/?$', DeleteView.as_view(), name='delete'),
)
