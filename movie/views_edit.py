from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from .models import Movie,Serial,SerialFilms,SerialSession,Review
from .forms import (
            FormMovie,FormSerialSession, FormSerial,
            FormSerialFilm,FormSerialFilm,FormReviewEdit
            )

def user_admin(user):
  return user.is_admin


@user_passes_test(user_admin)
@login_required
def edit_movie(request):
    if request.method == 'POST':
        obj = Movie.objects.get(slug=request.POST['slug'])
        form = FormMovie(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            cd = form.cleaned_data
            obj = form.save(commit=False)
            slti = cd['title']
            obj.slug = slti.replace(' ','-')
            obj.save() 
            return redirect(obj)
        else:
            form = FormMovie(request.POST, request.FILES)
            messages.warning(request,_("please chek field for error"))
            context = {
                'form':form,
            }
            return render(request, 'create/create.html', context)
    else:
        slug = request.GET.get('slug')
        obj = Movie.objects.get(slug=slug)
        form = FormMovie(instance=obj)
        return render(request, 'create/create.html', {'form':form})


@user_passes_test(user_admin)
@login_required
def edit_serial(request):
    if request.method == 'POST':
        obj = Serial.objects.get(slug=request.POST['slug'])
        form = FormSerial(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            cd = form.cleaned_data
            obj = form.save(commit=False)
            slti = cd['title']
            obj.slug = slti.replace(' ','-')
            obj.save() 
            return redirect(obj)
        else:
            form = FormMovie(request.POST, request.FILES)
            messages.warning(request,_("please chek field for error"))
            context = {
                'form':form,
            }
            return render(request, 'create/create.html', context)
    else:
        slug = request.GET.get('slug')
        obj = Serial.objects.get(slug=slug)
        form = FormSerial(instance=obj)
        return render(request, 'create/create.html', {'form':form})
 

@user_passes_test(user_admin)
@login_required
def edit_session(request):
    if request.method == 'POST':
        obj = SerialSession.objects.get(slug=request.POST['slug'])
        form = FormSerialSession(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            cd = form.cleaned_data
            obj = form.save(commit=False)
            slti = cd['title']
            obj.slug = slti.replace(' ','-')
            obj.save() 
            serial = Serial.objects.get(slug = obj.serial.slug)
            return redirect(serial)
        else:
            form = FormMovie(request.POST, request.FILES)
            messages.warning(request,_("please chek field for error"))
            context = {
                'form':form,
            }
            return render(request, 'create/create.html', context)
    else:
        pk = request.GET.get('pk')
        obj = SerialSession.objects.get(pk=pk)
        form = FormSerialSession(instance=obj)
        return render(request, 'create/create.html', {'form':form})


@user_passes_test(user_admin)
@login_required
def edit_category(request):
    pass


@user_passes_test(user_admin)
@login_required
def edit_relted_serial(request):
    if request.method == 'POST':
        obj = SerialFilms.objects.get(slug=request.POST['slug'])
        form = FormSerialFilm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            cd = form.cleaned_data
            obj = form.save(commit=False)
            slti = cd['title']
            obj.slug = slti.replace(' ','-')
            obj.save()
            serial = Serial.objects.get(slug = obj.serial.slug)
            return redirect(serial)
        else:
            form = FormMovie(request.POST, request.FILES)
            messages.warning(request,_("please chek field for error"))
            context = {
                'form':form,
            }
            return render(request, 'create/create.html', context)
    else:
        slug = request.GET.get('slug')
        obj = SerialFilms.objects.get(slug=slug)
        form = FormSerialFilm(instance=obj)
        return render(request, 'create/create.html', {'form':form})


@user_passes_test(user_admin)
@login_required
def edit_review(request):
        if request.method == 'POST':
            obj = Review.objects.get(slug=request.POST['slug'])
            form = FormReviewEdit(request.POST, request.FILES, instance=obj)
            if form.is_valid():
                cd = form.cleaned_data
                obj = form.save(commit=False)
                slti = cd['title']
                obj.slug = slti.replace(' ','-')
                obj.save() 
                form.save()
                return redirect(obj)
            else:
                form = FormMovie(request.POST, request.FILES)
                messages.warning(request,_("please chek field for error"))
                context = {
                    'form':form,
                }
                return render(request, 'create/create.html', context)
        else:
            slug = request.GET.get('slug')
            obj = Review.objects.get(slug=slug)
            form = FormReviewEdit(instance=obj)
            return render(request, 'create/create.html', {'form':form})