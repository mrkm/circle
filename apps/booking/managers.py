# -*- coding:utf-8 -*-
from google.appengine.ext import ndb
from booking.models import Booking


class Manager(object):
    kind = None

    @classmethod
    def get(cls, pk):
        # TODO: use memcache
        return ndb.Key(cls.kind, pk).get()

    @classmethod
    def delete(cls, pk):
        # TODO: use memcache
        return ndb.Key(cls.kind, pk).delete()


class BookingManager(Manager):
    kind = Booking

    @classmethod
    def fetch_by_state(cls, state):
        q = cls.kind.query()
        q = q.filter(cls.kind.state == state)
        q = q.order(cls.kind.start)
        # TODO: use memcache
        return q.fetch(100)

    @classmethod
    def check_overlap(cls, state, start, end):

        def _check(booking):
            if  start <= booking.start and booking.start < end:
                return False
            if  start < booking.end and booking.end <= end:
                return False
            return True

        bookings = cls.fetch_by_state(state)
        if not all([_check(booking) for booking in bookings]):
            return False
        return True
