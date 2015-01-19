# -*- coding: utf-8 -*-
import datetime
import hashlib
from google.appengine.api import memcache
from google.appengine.ext import ndb
from apps.core.utils import logger
from google.appengine.api import memcache

u"""
state
1: hakozaki,
2: ito,
11: hakozaki(calceled),
12: ito(calceled)
"""

class _ProhibitionRules(ndb.Model):
    name = ndb.StringProperty(required=False, indexed=False)
    start = ndb.DateTimeProperty(indexed=False)
    end = ndb.DateTimeProperty(indexed=False)
    state = ndb.IntegerProperty(indexed=False)

    def __unicode__(self):
        return '%s' % self.name


class _Booking(ndb.Model):
    name = ndb.StringProperty(required=False, indexed=False)
    start = ndb.DateTimeProperty(indexed=False)
    end = ndb.DateTimeProperty(indexed=False)
    state = ndb.IntegerProperty(indexed=False)
    password = ndb.StringProperty(indexed=False)

    def __unicode__(self):
        return '%s' % self.name


SORT_KEY = lambda booking: booking.start


class Booking(object):

    @staticmethod
    def get(pk):
        return ndb.Key(_Booking, pk).get()

    @staticmethod
    def delete(pk):
        #memcache.delete(cachekey)
        return ndb.Key(_Booking, pk).delete()

    @staticmethod
    def get_all():
        #bookings = memcache.get('bookings')
        #if bookings is not None:
        #    return bookings
        #memcache.set(cachekey)
        bookings = _Booking.query().fetch()
        east, west = [], []
        for booking in bookings:
            if booking.state == 1:
                east.append(booking)
            elif booking.state == 2:
                west.append(booking)
        east.sort(key=SORT_KEY)
        west.sort(key=SORT_KEY)
        #memcache.set('bookings', bookings, 60)
        return {'east': east, 'west': west}

    @staticmethod
    def create(name, start, end, state, password=""):
        return _Booking(name=name, start=start, end=end,
                        state=state, password=password).put()

    @classmethod
    def overlap(cls, state, start, end):
        def _check(bookings):
            for booking in bookings:
                if booking.start <= start and booking.end >= end:
                    raise Exception
            return True

        suspects = cls.get_all()
        if not all([_check(bookings) for bookings in suspects.values()]):
            return False
        return True

    @staticmethod
    def clean(data, cleaned_data, errors):
        try:
            cleaned_data[u"name"] = data[u"name"]
        except Exception, e:
            errors.append(u"name")

        try:
            time_ = int(data[u"time"])
        except Exception, e:
            errors.append(u"time")

        try:
            cleaned_data[u"length"] = int(data[u"length"])
        except Exception, e:
            errors.append(u"length")

        try:
            y, m, d = data[u"date"].split("-")
            date_ = datetime.date(int(y), int(m), int(d))
            cleaned_data["start"] = datetime.datetime(date_.year, date_.month, date_.day, time_)
            cleaned_data["end"] = cleaned_data["start"] + datetime.timedelta(hours=cleaned_data[u"length"])
        except Exception, e:
            errors.append(u"date")

        try:
            cleaned_data[u"room"] = int(data[u"room"])
        except Exception, e:
            errors.append(u"room")

        try:
            cleaned_data[u"password"] = hashlib.md5(data[u"pswd"]).hexdigest()
        except Exception, e:
            errors.append(u"password")

        if errors:
            raise Exception


TIME_CHOICES_EAST = ((8, u"8:00"),
                     (9, u"9:00"),
                     (10, u"10:00"),
                     (11, u"11:00"),
                     (12, u"12:00"),
                     (13, u"13:00"),
                     (14, u"14:00"),
                     (15, u"15:00"),
                     (16, u"16:00"),
                     (17, u"17:00"),
                     (18, u"18:00"),
                     (19, u"19:00"),
                     (20, u"20:00"),
                     )

TIME_CHOICES_WEST = ((7, u"7:30"),
                     (8, u"8:00"),
                     (9, u"9:00"),
                     (10, u"10:00"),
                     (11, u"11:00"),
                     (12, u"12:00"),
                     (13, u"13:00"),
                     (14, u"14:00"),
                     (15, u"15:00"),
                     (16, u"16:00"),
                     (17, u"17:00"),
                     (18, u"18:00"),
                     (19, u"19:00"),
                     (20, u"20:00"),
                     (21, u"21:00"),
                     )

LENGTH_CHOICES = ((1, u"1時間"),
                  (2, u"2時間"),
                  (3, u"3時間"),
                  )
"""
class BookingFrom(forms.Form):
    guest = forms.CharField(label=('Name'), required=True, widget=forms.TextInput(attrs={'placeholder': 'Penny Lane'}),)
    date = forms.DateField(label=('Date'), input_formats=('%Y%m%d',), required=True, widget=forms.TextInput(attrs={'placeholder': datetime.today().strftime('%Y%m%d')}),)
    length = forms.IntegerField(label=('Length'), widget=forms.Select(choices=LENGTH_CHOICES), required=True,)
    pswd = forms.CharField(label=('Password'), widget=forms.PasswordInput, required=False,)
    status = forms.CharField(label=('status'), initial=0, widget=forms.HiddenInput, required=True)

class BookingEastForm(BookingFrom):

    time = forms.IntegerField(label=('Time'), widget=forms.Select(choices=TIME_CHOICES_EAST), required=True,)

    def clean(self):
        errors = []
        ''' overlap '''
        date = self.cleaned_data.get('date', None)
        time = self.cleaned_data.get('time', None)
        length = self.cleaned_data.get('length', None)
        guest = self.cleaned_data.get('guest', None)

        try:
            datetime(date.year, date.month, date.day, time)
        except:
            errors.append('invaliddate')

        try:
            stdate = datetime(date.year, date.month, date.day, time)
            eddate = datetime(date.year, date.month, date.day, time+length)
            suspects = Booking.objects.filter(is_canceled=False,
                                              place = 0,
                                              stdate__year = date.year,
                                              stdate__month = date.month,
                                              stdate__day = date.day,
                                              )
            if suspects:
                for suspect in suspects:
                    if  stdate <= suspect.stdate and suspect.stdate < eddate:
                        errors.append('overlap')
                    if  stdate < suspect.eddate and suspect.eddate <= eddate:
                        errors.append('overlap')

            onemonthlater = datetime.today()+timedelta(days=31)
            if stdate >= onemonthlater:
                errors.append('onemonthlater')
        except:
            errors.append('unexpected1')

        try:
            if len(guest) > 30:
                errors.append('longname')
        except:
            errors.append('unexpected2')
        '''
        使用できる曜日は月火木金日です。
        水(2)、土(5)は他のサークルが防音室を利用してます。絶対に予約を入れないでください。
        '''
        try:
            forbid = [2, 5]
            if date.weekday() in forbid:
                errors.append('forbiddenweekday')
        except:
            errors.append('unexpected3')
        '''
        平日17時～21時
        休日9時～21時
        '''
        try:
            if date.weekday() < 5:
                if date.month in (8, 9):
                    pass
                else:
                    if stdate.hour < 17:
                        errors.append('forbiddenstarttime')
        except:
            errors.append('unexpected4')
        ''' add some rule '''

        try:
            if eddate.hour > 21:
                errors.append('forbiddenendtime')
        except:
            errors.append('unexpected5')

        if errors:
            raise forms.ValidationError(errors)
        return self.cleaned_data

    def save(self, force_insert=False, force_update=False):
        guest = self.cleaned_data['guest']
        date = self.cleaned_data['date']
        time = self.cleaned_data['time']
        length = self.cleaned_data['length']
        pswd = hashlib.md5(self.cleaned_data['pswd']).hexdigest()
        stdate = datetime(date.year, date.month, date.day, time)
        eddate = datetime(date.year, date.month, date.day, time+length)
        booking = Booking(guest=guest,
                          stdate=stdate,
                          eddate=eddate,
                          place=0,
                          att=0,
                          pswd=pswd,
                          )
        booking.save()
        return booking

class BookingWestForm(BookingFrom):

    time = forms.IntegerField(label=('Time'), widget=forms.Select(choices=TIME_CHOICES_WEST), required=True,)

    def clean(self):

        errors = []
        ''' overlap '''
        date = self.cleaned_data.get('date', None)
        time = self.cleaned_data.get('time', None)
        length = self.cleaned_data.get('length', None)
        guest = self.cleaned_data.get('guest', None)

        try:
            datetime(date.year, date.month, date.day, time)
        except:
            errors.append('invaliddate')

        try:
            stdate = datetime(date.year, date.month, date.day, time)
            eddate = datetime(date.year, date.month, date.day, time+length)
            suspects = Booking.objects.filter(is_canceled=False,
                                              place = 1,
                                              stdate__year = date.year,
                                              stdate__month = date.month,
                                              stdate__day = date.day,
                                              )
            if suspects:
                for suspect in suspects:
                    if  stdate <= suspect.stdate and suspect.stdate < eddate:
                        errors.append('overlap')
                    if  stdate < suspect.eddate and suspect.eddate <= eddate:
                        errors.append('overlap')
        except:
            errors.append('unexpected1')

        try:
            if len(guest) > 30:
                errors.append('longname')
        except:
            errors.append('unexpected2')

        '''
        7:30-22:00
        '''
        try:
            if eddate.hour > 22:
                errors.append('forbiddenendtime')
        except:
            errors.append('unexpected5')

        if errors:
            raise forms.ValidationError(errors)
        return self.cleaned_data


    def save(self, force_insert=False, force_update=False):
        guest = self.cleaned_data['guest']
        date = self.cleaned_data['date']
        time = self.cleaned_data['time']
        length = self.cleaned_data['length']
        pswd = hashlib.md5(self.cleaned_data['pswd']).hexdigest()
        stdate = datetime(date.year, date.month, date.day, time)
        eddate = datetime(date.year, date.month, date.day, time+length)
        booking = Booking(guest=guest,
                          stdate=stdate,
                          eddate=eddate,
                          place=1,
                          att=0,
                          pswd=pswd,
                          )
        booking.save()
        return booking
"""
