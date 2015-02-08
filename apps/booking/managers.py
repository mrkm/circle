# -*- coding:utf-8 -*-
import datetime
from google.appengine.ext import ndb
from booking.models import Booking


def today():
    now = datetime.datetime.now()
    return datetime.datetime(year=now.year, month=now.month, day=now.day)


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
        q = q.filter(cls.kind.start >= today())
        q = q.order(cls.kind.start)
        # TODO: use memcache
        return q.fetch(100)

    @classmethod
    def delete_old(cls, date):
        q = cls.kind.query()
        q = q.filter(cls.kind.start < date)
        ndb.delete_multi(q.fetch(100, keys_only=True))

    @classmethod
    def check_overlap(cls, state, start, end):

        def overlap(booking):
            if  start <= booking.start and booking.start < end:
                return True
            if  start < booking.end and booking.end <= end:
                return True
            return False

        bookings = cls.fetch_by_state(state)
        if any([overlap(booking) for booking in bookings]):
            return False
        return True
