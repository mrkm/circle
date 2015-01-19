from django.conf.urls import patterns, url, include

urlpatterns = patterns('',
    url(r'^$', 'booking.views.bookings', name='booking_bookings'),
    url(r'^check$', 'booking.views.check', name='booking_check'),
    url(r'^success$', 'booking.views.success', name='booking_success'),
    url(r'^cancel$', 'booking.views.cancel', name='booking_cancel'),
    url(r'^check_booking$', 'booking.views.check_booking', name='booking_check_booking'),
)
