from .models import User
from random import randint
from kavenegar import KavenegarAPI
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import UserPhoneForm, PasswordSms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate


#register and login and logout
def phone(request):
    if request.user.is_authenticated:
        return redirect('movie:index')

    if request.method == 'POST':
        form = UserPhoneForm(request.POST)
        if form.is_valid():
            global phone, rand_num
            phone = form.cleaned_data['phone_number']
            rand_num = randint(100000, 999999)
            #api = KavenegarAPI('Your APIKey', timeout=20)
            #params = {                    
            #        'sender':'number_get_of_kavenegar',
            #        'receptor':phone,
            #        'message':_(f'password for verify in site FREE-FILM:{rand_num}')
            #}
            #api.sms_send(params)
            print('phone:',phone,'sms',rand_num)
            messages.info(request,_("A text message was sent to your number"), 'info')
            return redirect('movie:sms')
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
    if request.method == 'POST':
        form = PasswordSms(request.POST)
        if form.is_valid():
            passwordraw = int(form.cleaned_data['password'])
            if passwordraw == rand_num:
                user_inc = User.objects.filter(phone_number = phone)
                if user_inc:
                    user = User.objects.get(phone_number = phone)
                    messages.success(request , _("your successfull to login in site"), 'success')
                    login(request, user)
                    return redirect('movie:index')
                else:
                    pass_in = f'@q+Z{rand_num}'
                    User.objects.create_user(phone_number = phone, password = pass_in).save()
                    user_auth = authenticate(request, phone_number= phone, password=pass_in)
                    messages.success(request , _("your successfull to login in site"), 'success')
                    login(request, user_auth)
                    return redirect('movie:index')
            if passwordraw != rand_num:
                messages.error(request, _("The password entered is incorrect"), 'error')
        else:
            form = PasswordSms(request.POST)
            messages.warning(request,_("please chek field for error"))
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

@login_required
def signout(request):
    logout(request)
    messages.success(request, _('you are logout of site'), 'success')
    return redirect('movie:phone')
