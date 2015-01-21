# -*- coding:utf-8 -*-
import datetime
import hashlib

class Form(object):
    cleaned_data = {}
    errors = []

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
            self.cleaned_data[u"room"] = int(data[u"room"])
        except Exception, e:
            self.errors.append(u"room")

        try:
            self.cleaned_data[u"password"] = hashlib.md5(data[u"pswd"]).hexdigest()
        except Exception, e:
            self.errors.append(u"password")

        return self
