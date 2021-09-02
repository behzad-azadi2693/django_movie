import random
from . import otp_check
from .models import User
from random import randint
from django.conf import settings
from django.contrib import messages
from datetime import date, datetime, tzinfo
from movie.models import SessionUser
from django.shortcuts import render, redirect
from .forms import UserPhoneForm, PasswordSms
from django.contrib.sessions.models import Session
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from rest_framework.authtoken.models import Token

def phone(request):
    if request.user.is_authenticated:
        return redirect('movie:index')

    if request.method == 'POST':
        form = UserPhoneForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone_number']
            otp = randint(100000, 999999)
            try:
                user = User.objects.get(phone_number = phone) 
                user.otp = otp
                user.save()
                #otp_check.sms_send(phone, otp)
                print('phone:',phone,'sms',otp)
                request.session['phone_number'] = user.phone_number
                messages.info(request,_("A text message was sent to your number"), 'info')
                return redirect('accounts:sms')
            except User.DoesNotExist:
                passwrd = 'Asdsfe3434932n#$2'
                user = User.objects.create_user(phone_number = phone,  password = passwrd)
                user.is_active = False
                user.otp = otp
                user.save()
                #otp_check.sms_send(phone, otp)
                print('phone:',phone,'sms',otp)
                request.session['phone_number'] = user.phone_number
                messages.info(request,_("A text message was sent to your number"), 'info')
                return redirect('sccounts:sms')
        else:
            form = UserPhoneForm(request.POST)
            messages.warning(request,_("please chek field for error"))
            context = {
                'form':form,
            }
            return render(request, 'signin/phone_number.html', context)
    else:
        form = UserPhoneForm()

    context = {
        'form':form,
    }

    return render(request, 'signin/phone_number.html', context)



def sms(request):
    if request.user.is_authenticated:
        return redirect('movie:index')     

    try:
        phone = request.session.get('phone_number')
        user = User.objects.get(phone_number = phone)

        if request.method == 'POST':
            form = PasswordSms(request.POST)
            if form.is_valid():
                passwordraw = int(form.cleaned_data['password'])
                if passwordraw == user.otp and user.otp is not None:
                    if not otp_check.check_time(phone):
                        messages.warning(request,_('time for check password out'),'error')
                        return redirect('accounts:phone')

                    user.is_active = True
                    user.otp = None
                    user.save()
                    del request.session['phone_number']
                    messages.success(request , _("your successfull to login in site"), 'success')
                    login(request, user)
                    SessionUser.objects.get_or_create(
                                        user = user,
                                        session_key =Session.objects.get(session_key = request.session.session_key),
                                        device = f'{request.user_agent.browser.family}-{request.user_agent.browser.version_string}',
                                        os = f'{request.user_agent.os.family}-{request.user_agent.os.version_string}',
                                        date_joiin = date.today(),
                                        ip_device =request.META['REMOTE_ADDR'] ,
                                    )
                    Token.objects.get_or_create(user=user)
                    return redirect('movie:index')
                if passwordraw != user.otp:
                    messages.error(request, _("The password entered is incorrect"), 'error')
            else:
                form = PasswordSms(request.POST)
                messages.warning(request,_("please chek field for error"),'error')
                context = {
                    'form':form,
                }
                return render(request, 'signin/sms.html', context)
        else:
            form = PasswordSms()
            context = {
                'form':form,
            }
            return render(request, 'signin/sms.html', context)

    except User.DoesNotExist:
        return redirect('movie:phone')




@login_required
def signout(request):
    logout(request)
    messages.success(request, _('you are logout of site'), 'success')
    return redirect('accounts:phone')
