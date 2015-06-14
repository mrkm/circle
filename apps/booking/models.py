# -*- coding: utf-8 -*-
from google.appengine.ext import ndb


class Booking(ndb.Model):
    name = ndb.StringProperty(required=False, indexed=False)
    start = ndb.DateTimeProperty(indexed=True)
    end = ndb.DateTimeProperty(indexed=False)
    state = ndb.StringProperty(indexed=True)
    password = ndb.StringProperty(indexed=False)

    def __unicode__(self):
        return '%s %s %s-%s' % (
            self.name,
            self.start.strftime("%a %-m/%-d"),
            self.start.strftime("%-H"),
            self.end.strftime("%-H"))
