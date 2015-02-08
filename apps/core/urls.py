from django.conf.urls import patterns, url
from views import TopView, DeleteView, ManageView


urlpatterns = patterns('',
    url(r'^$', TopView.as_view(), name='home'),
    url(r'^manage$', ManageView.as_view(), name='manage'),
    url(r'^delete/(?P<pk>\d+)/?$', DeleteView.as_view(), name='delete'),
)
