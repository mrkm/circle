# -*- coding:utf-8 -*-
import datetime
import hashlib
import const

class Form(object):
    cleaned_data = {}
    errors = []

    @classmethod
    def check_available(cls, room, start, end):
        if room == const.EAST:
            available = const.AVAILABLE_EAST[start.weekday()]
        else:
            available = const.AVAILABLE_WEST[start.weekday()]
        assert start.time() >= available[0]
        assert end.time() <= available[1]

    def clean(self, data):
        try:
            self.cleaned_data[u"name"] = data[u"name"]
        except Exception, e:
            self.errors.append(u"name")

        try:
            time_ = int(data[u"time"])
        except Exception, e:
            self.errors.append(u"time")

        try:
            self.cleaned_data[u"length"] = int(data[u"length"])
        except Exception, e:
            self.errors.append(u"length")

        try:
            y, m, d = data[u"date"].split("-")
            date_ = datetime.date(int(y), int(m), int(d))
            self.cleaned_data["start"] = datetime.datetime(
                date_.year, date_.month, date_.day, time_)
            self.cleaned_data["end"] = self.cleaned_data["start"] + datetime.timedelta(
                hours=self.cleaned_data[u"length"])
        except Exception, e:
            self.errors.append(u"date")

        try:
            self.cleaned_data[u"room"] = data[u"room"]
            assert self.cleaned_data[u"room"] in [const.EAST, const.WEST]
        except Exception, e:
            self.errors.append(u"room")

        try:
            self.check_available(self.cleaned_data[u"room"],
                                 self.cleaned_data[u"start"],
                                 self.cleaned_data[u"end"])
        except Exception, e:
            self.errors.append(u"date")

        try:
            self.cleaned_data[u"password"] = hashlib.md5(data[u"pswd"]).hexdigest()
        except Exception, e:
            self.errors.append(u"password")

        return self
