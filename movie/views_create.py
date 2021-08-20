import datetime
from django.contrib import messages
from django.core.mail import send_mail
from django.http.response import BadHeaderError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from .models import (
            Movie,Serial,SerialFilms,
            SerialSession,Review, Category,
            NewsLetters, MessagesSending,
            )
from .forms import (
            FormMovie,FormSerialSession, FormSerial,
            FormCategory,FormSerialFilm,FormSerialFilm,
            FormReview
            )


def user_admin(user):
    return user.is_admin

@user_passes_test(user_admin)
@login_required
def admin_create(request):
        return render(request, 'create/admin_create.html')

@user_passes_test(user_admin)
@login_required
def create_movie(request):
    if request.method == 'POST':
        form = FormMovie(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            movie = Movie.objects.create(
                name = cd['name'],name_en = cd['name_en'], title = cd['title'], gener =cd['gener'],
                gener_en = cd['gener_en'], description = cd['description'], description_en = cd['description_en'],
                image = cd['image'], filmpas = cd['filmpas'], subtitle = cd['subtitle'],
                film1080 = cd['film1080'], filme720 = cd['filme720'], film480=cd['film480'],
                date = cd['date'], ratin = cd['ratin'], awards = cd['awards'], time = cd['time'],
                category = cd['category'], choice = cd['choice'], director = cd['director'],
                writer = cd['writer'], stars = cd['stars']
            )
            movie.save()
            return redirect(movie)
        else:
            form = FormMovie(request.POST, request.FILES)
            messages.warning(request,_("please chek field for error"))
            context = {
                'form':form,
            }
            return render(request, 'create/create.html', context)
    else:
        form = FormMovie()
    context = {
        'form':form,
    }
    return render(request, 'create/create.html', context)


@user_passes_test(user_admin)
@login_required
def create_serial(request):
    if request.method == 'POST':
        form = FormSerial(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            serial = Serial.objects.create(
                name = cd['name'],name_en = cd['name_en'], title = cd['title'], gener =cd['gener'],
                gener_en = cd['gener_en'], description = cd['description'], description_en = cd['description_en'],
                image = cd['image'], filmpas = cd['filmpas'],
                date = cd['date'], ratin = cd['ratin'], awards = cd['awards'], time = cd['time'],
                category = cd['category'], choice = cd['choice'], director = cd['director'],
                writer = cd['writer'], stars = cd['stars']
            )
            serial.save()
            return redirect(serial)
        else:
            form = FormSerial(request.POST, request.FILES)
            messages.warning(request,_("please chek field for error"))
            context = {
                'form':form,
            }
            return render(request, 'create/create.html', context)    
    else:
        form = FormSerial()
    context = {
        'form':form,
    }
    return render(request, 'create/create.html', context)
    
       
 
@user_passes_test(user_admin)
@login_required
def create_session(request):
    if request.method == 'POST':
        form = FormSerialSession(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            session = SerialSession.objects.create(
                title = cd['title'],session = cd['session'],
                serial = cd['serial'], subtitle = cd['subtitle'],
            )
            session.save()
            serial = Serial.objects.get(slug = session.serial.slug)
            return redirect(serial)
        else:
            form = FormSerialSession(request.POST, request.FILES)
            messages.warning(request,_("please chek field for error"))
            context = {
                'form':form,
            }
            return render(request, 'create/create.html', context)
    else:
        pk = request.GET.get('pk')
        obj = Serial.objects.get(pk = pk)
        data = {'serial': obj }
        form = FormSerialSession(initial=data)
    context = {
        'form':form,
    }
    return render(request, 'create/create.html', context)



@user_passes_test(user_admin)
@login_required
def create_category(request):
    if request.method == 'POST':
        form = FormCategory(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            Category.objects.create(name = cd['name'], name_en = cd['name_en'])
            return redirect('movie:create')
        else:
            form = FormMovie(request.POST)
            messages.warning(request,_("please chek field for error"))
            context = {
                'form':form,
            }
            return render(request, 'create/create.html', context)
    else:
        form = FormCategory()
    context = {
        'form':form,
    }
    return render(request, 'create/create.html', context)
    

@user_passes_test(user_admin)
@login_required
def create_related_serial(request):
    if request.method == 'POST':
        form = FormSerialFilm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            serial = SerialFilms.objects.create(
                        episod = cd['episod'], title = cd['title'],
                        serial = cd['serial'], session = cd['session'], serial1080 = cd['serial1080'],
                        serial720 = cd['serial720'], serial480=cd['serial480']
                    )
            serial.save()
            serial = Serial.objects.get(slug = serial.serial.slug)
            return redirect(serial)
    else:
        pk_serial = request.GET.get('serial')
        pk_session = request.GET.get('session')
        obj_serial = Serial.objects.get(pk = pk_serial)
        obj_session = SerialSession.objects.get(pk = pk_session)
        data = {'serial': obj_serial, 'session':obj_session }
        form = FormSerialFilm(initial=data)
    context = {
        'form':form,
    }
    return render(request, 'create/create.html', context)


@user_passes_test(user_admin)
@login_required
def create_review_movie(request):
    if request.method == 'POST':
        form = FormReview(request.POST, request.FILES)
        if form.is_valid():
            cd  = form.cleaned_data
            movie = Movie.objects.get(pk=cd['pk'])
            review = Review(
                title = cd['title'],description=cd['description'],description_en = cd['description_en'],
                filmpas = cd['filmpas'], content_object = movie, is_for = cd['is_for'], name=movie.name,
                choice = movie.choice, name_en = movie.name_en
            ) 
            review.save()
            return redirect(review)
    else:
        is_for = request.GET.get('is_for')
        pk = request.GET.get('pk')
        data = {'is_for':is_for,'pk':pk}
        form = FormReview(initial=data)
    context = {
        'form':form,
    }
    return render(request, 'create/create.html', context)


@user_passes_test(user_admin)
@login_required
def create_review_serial(request):
    if request.method == 'POST':
        form = FormReview(request.POST, request.FILES)
        if form.is_valid():
            cd  = form.cleaned_data
            movie = Serial.objects.get(pk=cd['pk'])
            review = Review(
                title = cd['title'],description=cd['description'],description_en = cd['description_en'],
                filmpas = cd['filmpas'], content_object = movie, is_for = cd['is_for'], name=movie.name,
                choice = movie.choice, name_en=movie.name_en
            )
            review.save()
            return redirect(review)
    else:
        is_for = request.GET.get('is_for')
        pk = request.GET.get('pk')
        data = {'is_for':is_for,'pk':pk}
        form = FormReview(initial=data)
    context = {
        'form':form,
    }
    return render(request, 'create/create.html', context)




def email(request):
    if request.method == 'POST':
        path = request.POST.get('next')
        email = request.POST.get('email')
        email_has = NewsLetters.objects.filter(email=email)
        if email_has:
            messages.warning(request, _('email is exist '), 'error')
            return redirect(path)

        if email:
            NewsLetters.objects.create(email=request.POST.get('email'))
            messages.success(request, _('Your email has been successfully registered'), 'success')
            return redirect(path)

    messages.warning(request,_('please full the input with your email'))
    return redirect('movie:index')


@user_passes_test(user_admin)
@login_required
def send_email(request):
    if request.method == 'POST':
        subject = request.POST.get('subject') or None
        date = datetime.datetime.now()
        message = request.POST.get('message') or None
        if subject is not None and message is not None:
            MessagesSending.objects.create(subject = subject, date=date, messages=message)

            receiver = []
            for user in NewsLetters.objects.all():
                receiver.append(user.email)

            try:
                send_mail(
                    subject,
                    message,
                    'FreeFilm Site',
                    receiver,
                    fail_silently=False,
                )
                
                messages.success(request,_('email sendig successfully'), 'succsess')
                return redirect('movie:create')

            except BadHeaderError:
                messages.warning(request,_('email not sendig successfully'),'error')
                return redirect('movie:create')
        else:
            messages.warning(request,_('please check fields all full'), 'error')
            return redirect('movie:create')

    return redirect('movie:create')