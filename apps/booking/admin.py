# -*- coding:utf-8 -*-
from django.contrib import admin
from booking.models import Booking

class BookingAdmin(admin.ModelAdmin):    
    list_filter = ('guest',)
    list_display = ('guest',)
    search_fields = ['guest']

admin.site.register(Booking, BookingAdmin)

from django.conf.urls.defaults import *



