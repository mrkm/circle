# -*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from forms import BookingEastForm, BookingWestForm, BookingCancelForm
from django.conf import settings
from booking.models import Booking
from datetime import date, timedelta
from django.template import RequestContext
from django_utils.utils import response



def check_booking(req):
    if req.method == 'POST':
        y = req.POST.get('y', None)
        m = req.POST.get('m', None)
        d = req.POST.get('d', None)
        s = req.POST.get('s', None)
        e = req.POST.get('e', None)
        l = req.POST.get('l', None)
        
        for exist in [y, m, d, s, e, l]:
            if not exist:
                return HttpResponse("false", 'text/javascript')

        # suspects = Booking.objects.filter(is_canceled=False,
        #                                   place = 0,
        #                                   stdate__year = date.year,
        #                                   stdate__month = date.month,
        #                                   stdate__day = date.day,
        #                                   )
        # if suspects:
        #     for suspect in suspects:
        #         if  stdate <= suspect.stdate and suspect.stdate <= eddate:
        #             errors.append('overlap')
        #         if  stdate <= suspect.eddate and suspect.eddate <= eddate:
        #             errors.append('overlap')
        return HttpResponse("true", 'text/javascript')
    else:
        return HttpResponse("", 'text/javascript')

def set_errors(form, v):
    if form.errors.get('__all__', None):
        for key in form.errors['__all__']:
            v[key] = True
    v['error'] = True
    return v

def get_bookings(place):
    return Booking.objects.filter(stdate__gte=date.today()).filter(is_canceled=False, place=place).order_by('stdate')

def bookings(req):
    v = {}
    bookings = []
    if req.method == "POST":
        place = req.POST.get('place', None)
        if place == '0':
            template = 'booking/east/lists.html'
            form = BookingEastForm(req.POST)
        elif place=='1':
            template = 'booking/west/lists.html'
            form = BookingWestForm(req.POST)
        else:
            return response(req, '404.html', v)    

        if form.is_valid():
            req.session['post'] = req.POST
            return HttpResponseRedirect(reverse('booking_check'))
        else:
            v = set_errors(form, v.copy())
            v['date'] = date.today().strftime('%Y%m%d')
            v['onemonthlaterdate'] = date.today()+timedelta(days=31)
            #v['post'] = req.POST
    else:
        place = req.REQUEST.get('l', None)

        if place == '0':
            template = 'booking/east/lists.html'
            form = BookingEastForm()
        elif place=='1':
            template = 'booking/west/lists.html'
            form = BookingWestForm()
        else:
            return response(req, '404.html', v)

    v['bookings'] =  get_bookings(place)
    v['form'] = form
    return response(req, template, v)    

def check(req):
    '''
    '''
    v = {}
    post = req.session['post']
    
    if post.get('place', None)=='0':
        form = BookingEastForm(post)
        template = 'booking/east/check.html'
    elif post.get('place', None)=='1':
        form = BookingWestForm(post)
        template = 'booking/west/check.html'

    #v['post'] = post
    v['form'] = form
    v['date'] = '%s-%s-%s' % (post['date'][:4], post['date'][4:6], post['date'][6:])
    v['time'] = '%s-%s' % (int(post['time']), int(post['time'])+int(post['length']))
    if post['pswd']:        
        v['pswd'] = "*"*len(post['pswd'])
    else:
        v['pswd'] = u"パスワードは設定されていません"
    if ( req.method == 'POST' ):
        if ( req.POST.get('store', None) ):
            form.is_valid()
            form.save()
            post = post.copy()
            post['sucess'] = u'予約を作成しました'
            req.session['post'] = post
            return HttpResponseRedirect(reverse('home'))

    return response(req, template, v)

def success(req):
    '''
    '''
    v = {}
    v['post'] = req.session['post']


    return response(req, 'booking/success.html', v)

def cancel(req):
    if req.method=='POST':
        v = {}
        post = req.session.get('post', {})
        v['post'] = post
        bid = req.REQUEST.get('id')
        target = Booking.objects.filter(id=bid)[0]
        if target.stdate.hour == 7:
            v['time'] = '7:30-%s:00' % (target.eddate.hour)
        else:
            v['time'] = '%s:00-%s:00' % (target.stdate.hour, target.eddate.hour)
        if target.place == '0':
            v['place'] = u'箱崎'
        if target.place == '1':
            v['place'] = u'伊都'
        v['date'] = '%s-%s-%s' % (target.stdate.year, target.stdate.month, target.stdate.day)
        if target.place == '0':
            template = 'booking/east/cancel.html'
        elif target.place == '1':
            template = 'booking/west/cancel.html'
        else:
            template = '404.html'
        form = BookingCancelForm(req.POST,target)
        if form.is_valid():
            form.save()
            v['status'] = 'success'            
            post = post.copy()
            post['sucess'] = u'予約をキャンセルしました'
            req.session['post'] = post
            return HttpResponseRedirect(reverse('home'))
        else:
            v = set_errors(form, v.copy())
            v['form'] = form
            v['target'] = target
            if post.get('failed', None):
                v['hint'] = True
            post = post.copy()
            post['failed'] = True
            req.session['post'] = post
            return render_to_response(template, v, context_instance=RequestContext(req))
    else:
        v = {}
        bid = req.REQUEST.get('id')
        target = Booking.objects.filter(id=bid)[0]
        if target.place == '0':
            template = 'booking/east/cancel.html'
        elif target.place == '1':
            template = 'booking/west/cancel.html'
        else:
            template = '404.html'
        form = BookingCancelForm(req.POST, target)
        v['form'] = form
        v['target'] = target
        return render_to_response(template , v, context_instance=RequestContext(req))
