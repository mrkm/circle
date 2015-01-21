# -*- coding: utf-8 -*-
# coding: utf-8
import datetime
from django.conf import settings
from django.http import HttpResponseRedirect
from libs.django_utils.utils import BaseView as DjangoView
from apps.core.utils import logger
from apps.booking import const
from apps.booking.forms import Form
from apps.booking.managers import BookingManager
from apps.booking.models import Booking


def datetime_options(base_date, num=14):
    option = u"<option value='%s'>%s</option>"
    options = u""
    for i in xrange(num):
        date_ = (base_date + datetime.timedelta(i))
        options += option % (date_.isoformat(), date_.strftime("%a %m/%d"))
    return options


class BaseView(DjangoView):
    def render_to_response(self, context):
        context["CONTACT_EMAIL"] = settings.CONTACT_EMAIL
        return super(BaseView, self).render_to_response(context)


class DeleteView(BaseView):
    template_name = "core/delete.html"
    http_method_names = [u"get", u"post"]

    def get(self, request, pk):
        booking = BookingManager.get(int(pk))
        if booking is None:
            return HttpResponseRedirect("/")
        context = {}
        context['booking'] = booking
        return self.render_to_response(context)

    def post(self, request, pk):
        try:
            BookingManager.delete(int(pk))
        except:
            pass
        return HttpResponseRedirect("/")


class TopView(BaseView):
    template_name = "core/top.html"
    http_method_names = [u"get", u"post"]

    def _render(self, _context):
        context = {}
        context.update(_context)
        context["east"] = BookingManager.fetch_by_state(const.EAST)
        context["west"] = BookingManager.fetch_by_state(const.WEST)
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
        return Booking(name=name, start=start, end=end,
                       state=state, password=password).put()

    def form_clean(self, data):
        errors = []
        form = Form().clean(data)
        if form.errors:
            return None, form.errors

        if not BookingManager.check_overlap(
            form.cleaned_data[u"room"], form.cleaned_data["start"], form.cleaned_data["end"]):
            return None, ["overlap"]

        return form.cleaned_data, []
