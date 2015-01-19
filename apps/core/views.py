# -*- coding: utf-8 -*-
# coding: utf-8
import datetime
from django.http import HttpResponseRedirect
from libs.django_utils.utils import BaseView
from apps.core.utils import logger
from apps.booking.models import Booking


def datetime_options(base_date, num=14):
    option = u"<option value='%s'>%s</option>"
    options = u""
    for i in xrange(num):
        date_ = (base_date + datetime.timedelta(i))
        options += option % (date_.isoformat(), date_.strftime("%a %m/%d"))
    return options


class DeleteView(BaseView):
    template_name = "core/delete.html"
    http_method_names = [u"get", u"post"]

    def get(self, request, pk):
        booking = Booking.get(int(pk))
        if booking is None:
            return HttpResponseRedirect("/")
        context = {}
        context['booking'] = booking
        return self.render_to_response(context)

    def post(self, request, pk):
        try:
            Booking.delete(int(pk))
        except:
            pass
        return HttpResponseRedirect("/")


class TopView(BaseView):
    template_name = "core/top.html"
    http_method_names = [u"get", u"post"]

    def _render(self, _context):
        context = {}
        context.update(_context)
        bookings = Booking.get_all()
        context["east"] = bookings.get("east")
        context["west"] = bookings.get("west")
        context["datetime_options"] = datetime_options(datetime.date.today())
        context["post"] = ""
        return self.render_to_response(context)

    def get(self, request):
        u"""
        top page
        URL: /
        """
        return self._render({})

    def post(self, request):
        context = {}
        cleaned_data, errors = self.form_clean(request.POST)
        if errors:
            context["errors"] = errors
            return self._render(context)
        booking = self.create(cleaned_data)
        return HttpResponseRedirect("/")

    def create(self, cleaned_data):
        name = cleaned_data.get(u"name")
        date_ = cleaned_data.get(u"date")
        time_ = cleaned_data.get(u"time")
        length = cleaned_data.get(u"length")
        state = cleaned_data.get(u"room")
        password = cleaned_data.get(u"password")
        start = cleaned_data.get("start")
        end = cleaned_data.get("end")
        return Booking.create(name, start, end, state)

    def form_clean(self, data):
        cleaned_data = {}
        errors = []
        try:
            Booking.clean(data, cleaned_data, errors)
        except Exception, e:
            return None, errors
        try:
            Booking.overlap(cleaned_data[u"room"], cleaned_data["start"], cleaned_data["end"])
        except Exception, e:
            errors.append(u"overlap")
            return None, errors

        return cleaned_data, errors
