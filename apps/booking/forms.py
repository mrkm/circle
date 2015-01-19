# -*- coding:utf-8 -*-

from django import forms
from django.conf import settings
from django.utils.translation import ugettext as _
from booking.models import Booking
from booking.utils import checkoverlap
from datetime import datetime, timedelta
import hashlib

TIME_CHOICES_EAST = ((8, '8:00'),
                     (9, '9:00'),
                     (10, '10:00'),
                     (11, '11:00'),
                     (12, '12:00'),
                     (13, '13:00'),
                     (14, '14:00'),
                     (15, '15:00'),
                     (16, '16:00'),
                     (17, '17:00'),
                     (18, '18:00'),
                     (19, '19:00'),
                     (20, '20:00'),
                     )

TIME_CHOICES_WEST = ((7, '7:30'),
                     (8, '8:00'),
                     (9, '9:00'),
                     (10, '10:00'),
                     (11, '11:00'),
                     (12, '12:00'),
                     (13, '13:00'),
                     (14, '14:00'),
                     (15, '15:00'),
                     (16, '16:00'),
                     (17, '17:00'),
                     (18, '18:00'),
                     (19, '19:00'),
                     (20, '20:00'),
                     (21, '21:00'),
                     )

LENGTH_CHOICES = ((1, '1時間'),
                  (2, '2時間'),
                  (3, '3時間'),
                  )

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

class BookingCancelForm(forms.Form):
    
    pswd = forms.CharField(label=_(u'パスワード'),
                           widget=forms.PasswordInput,
                           required=False,
                           )
    bid =  forms.CharField()
    
    def clean(self):
        errors = []
        booking = Booking.objects.filter(id=self.cleaned_data['bid'])[0]
        try:
            pswd = self.cleaned_data['pswd']
        except:
            pswd = ''
        if not booking.pswd == hashlib.md5(pswd).hexdigest():
            errors.append('invalidpswd')
        if errors:
            raise forms.ValidationError(errors)
        return self.cleaned_data

    def save(self):
        booking = Booking.objects.filter(id=self.cleaned_data['bid'])[0]
        try:
            pswd = self.cleaned_data['pswd']
        except:
            pswd = ''
        if booking.pswd == hashlib.md5(pswd).hexdigest():
            booking.is_canceled=True
            booking.save()
        return booking
