# coding: utf-8
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.conf import settings
from django.views.generic import base

def redirect_message(req, url, message=""):
    # messages.add_message(req, level, message)
    req.session['msg'] = message
    return HttpResponseRedirect(url)


def response(req, temp_path, v, mime_type=settings.DEFAULT_CONTENT_TYPE):
    return render_to_response(temp_path, v, mimetype=mime_type, context_instance=RequestContext(req))


class BaseView(base.TemplateResponseMixin, base.View):
    template_name = ''
