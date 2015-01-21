# -*- coding: utf-8 -*-
from google.appengine.ext import ndb


class Booking(ndb.Model):
    name = ndb.StringProperty(required=False, indexed=False)
    start = ndb.DateTimeProperty(indexed=True)
    end = ndb.DateTimeProperty(indexed=False)
    state = ndb.IntegerProperty(indexed=True)
    password = ndb.StringProperty(indexed=False)

    def __unicode__(self):
        return '%s' % self.name
