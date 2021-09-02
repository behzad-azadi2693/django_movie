import random
from accounts import otp_check
from accounts.models import User
from random import randint
from django.conf import settings
from django.contrib import messages
from datetime import date, datetime, tzinfo
from movie.models import SessionUser
from django.shortcuts import render, redirect
from django.contrib.sessions.models import Session
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from .seializer_user import OtpSerializer,PhoneSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status, views


@api_view(['GET','POST'])
def phone(request):
    if request.user.is_authenticated:
        return redirect('api:index')

    if request.method == 'POST':
        form = PhoneSerializer(data=request.data)
        if form.is_valid():
            phone = request.data['phone_number']
            otp = randint(100000, 999999)
            try:
                user = User.objects.get(phone_number = phone) 
                user.otp = otp
                user.save()
                #otp_check.sms_send(phone, otp)
                print('phone:',phone,'sms',otp)
                request.session['phone_number'] = user.phone_number
                return redirect('api:sms')
            except User.DoesNotExist:
                passwrd = 'Asdsfe3434932n#$2'
                user = User.objects.create_user(phone_number = phone,  password = passwrd)
                user.is_active = False
                user.otp = otp
                user.save()
                #otp_check.sms_send(phone, otp)
                print('phone:',phone,'sms',otp)
                request.session['phone_number'] = user.phone_number
                return redirect('api:sms')
        else:
            form_new = PhoneSerializer().data
            srz = (form.errors, form_new)
            return Response(srz, status=status.HTTP_400_BAD_REQUEST)
        
    else:
        form = PhoneSerializer()
        return Response(form.data)


@api_view(['GET','POST'])
def sms(request):
    if request.user.is_authenticated:
        return redirect('api:index')

    try:
        phone = request.session.get('phone_number')
        user = User.objects.get(phone_number = phone)

        if request.method == 'POST':
            form = OtpSerializer(data=request.data)
            if form.is_valid():
                passwordraw = int(request.data['otp'])
                if passwordraw == user.otp and user.otp is not None:
                    if not otp_check.check_time(phone):
                        return redirect('api:phone')

                    user.is_active = True
                    user.otp = None
                    user.save()
                    del request.session['phone_number']
                    login(request, user)
                    SessionUser.objects.get_or_create(
                                        user = user,
                                        session_key =Session.objects.get(session_key = request.session.session_key),
                                        device = f'{request.user_agent.browser.family}-{request.user_agent.browser.version_string}',
                                        os = f'{request.user_agent.os.family}-{request.user_agent.os.version_string}',
                                        date_joiin = date.today(),
                                        ip_device =request.META['REMOTE_ADDR'] ,
                                    )
                    return redirect('api:index')
                if passwordraw != user.otp:
                    return redirect('api:sms')
            else:
                form_new = OtpSerializer().data
                srz = (form_new, form.errors)
                return Response(srz, status=status.HTTP_400_BAD_REQUEST)

        else:
            form = OtpSerializer()
            return Response(form.data)

    except User.DoesNotExist:
        return redirect('api:phone')




@login_required
def signout(request):
    logout(request)
    messages.success(request, _('you are logout of site'), 'success')
    return redirect('accounts:phone')


'''
from accounts.models import User
from .models import Serial, Movie, Save
from django.contrib.sessions.models import Session
from django.shortcuts import get_object_or_404



def user(request):
    pk = request.user.pk
    user = get_object_or_404(User, pk=pk)
    information = user.sessions.all()
    paid_history = user.history_paid.all()
    saves = Save.objects.filter(user = request.user)

    context = {
        'user':user,
        'informations':information,
        'saves':saves,
        'paids':paid_history,
    }

    return render(request, 'publick/user.html', context)


def remove_session(request):
    if request.method == 'POST':
        key = request.POST.get('key')
        try:
            session = Session.objects.get(session_key = key)
            session.delete()
            return redirect('movie:user')
        except:
            return redirect('movie:user')
    else:           
        return redirect('movie:user')
'''
