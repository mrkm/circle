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


def datetime_options(base_date, num=30):
    option = u"<option value='%s'>%s</option>"
    options = u""
    for i in xrange(num):
        date_ = (base_date + datetime.timedelta(i))
        options += option % (date_.isoformat(), date_.strftime("%a %-m/%-d"))
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


class ManageView(BaseView):
    template_name = "core/top.html"
    http_method_names = [u"get"]

    def get(self, request):
        date = datetime.datetime.now()
        BookingManager.delete_old(datetime.datetime(
                year=date.year, month=date.month, day=1))
        return self.render_to_response({})


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
        cleaned_data, errors, message = self.form_clean(request.POST)
        if errors:
            context["errors"] = errors
            context["message"] = message
            context["posted"] = cleaned_data
            return self._render(context)
        key = self.create(cleaned_data)
        booking = key.get()
        context["message"] = u"予約しました。%s" % booking
        context["success"] = True
        #return HttpResponseRedirect("/")
        return self._render(context)

    def create(self, cleaned_data):
        return Booking(
            name=cleaned_data.get(u"name"),
            start=cleaned_data.get("start"),
            end=cleaned_data.get("end"),
            state=cleaned_data.get(u"room"),
            password=cleaned_data.get(u"password")).put()

    def form_clean(self, data):
        errors = []
        form = Form().clean(data)
        if form.errors:
            return (form.cleaned_data, form.errors, form.message)

        overlap = BookingManager.check_overlap(
            form.cleaned_data[u"room"],
            form.cleaned_data["start"],
            form.cleaned_data["end"])
        if overlap:
            return (form.cleaned_data,
                    ["overlap"], u"別な予約と重なっています。 %s" % overlap)

        return (form.cleaned_data, [], "")
