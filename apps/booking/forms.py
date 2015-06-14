# -*- coding:utf-8 -*-
import datetime
import hashlib
import const
import logging

logger = logging.getLogger(__name__)


class Form(object):
    cleaned_data = None
    errors = None
    message = None

    def __init__(self):
        super(Form, self).__init__()
        self.errors = []
        self.cleaned_data = {}

    @classmethod
    def check_available(cls, room, start, end):
        if room == const.EAST:
            available = const.AVAILABLE_EAST[start.weekday()]
        else:
            available = const.AVAILABLE_WEST[start.weekday()]
        if not (start.time() >= available[0] and end.time() <= available[1]):
            return u"%s-%s" % (available[0], available[1])
        return None

    def clean(self, data):
        try:
            assert len(data[u"name"]) > 0
            self.cleaned_data[u"name"] = data[u"name"]
        except Exception, e:
            self.errors.append(u"name")
            self.message = u"予約名を入力してください。"

        _time = int(data[u"time"])
        _length = int(data[u"length"])

        y, m, d = data[u"date"].split("-")
        _date = datetime.date(int(y), int(m), int(d))
        self.cleaned_data["start"] = datetime.datetime(
            _date.year, _date.month, _date.day, _time)
        self.cleaned_data["end"] = self.cleaned_data["start"] + datetime.timedelta(
            hours=_length)

        self.cleaned_data[u"room"] = data[u"room"]
        check = self.check_available(self.cleaned_data[u"room"],
                                     self.cleaned_data[u"start"],
                                     self.cleaned_data[u"end"])
        if check:
            if self.cleaned_data[u"room"] == const.EAST:
                _room = u"箱崎"
            else:
                _room = u"伊都"
            self.errors.append(u"date")
            self.message = u"%s(%s)の予約可能時間は%sです。" % (
                _date.strftime("%a %-m/%-d"), _room, check)

        try:
            self.cleaned_data[u"password"] = hashlib.md5(data[u"pswd"]).hexdigest()
        except Exception, e:
            self.errors.append(u"password")

        return self
