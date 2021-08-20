from itertools import chain
from django.db.models import Q
from django.conf import settings
from .forms import FormContactForm
from django.core.cache import cache
from django.contrib import messages
from django.utils import translation
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import ( 
                    Movie, ContactUs, Serial, SerialFilms,
                    SerialSession, Review
                )


def change_language(request):
    if request.method == 'POST':
        lang = request.POST.get('language')
        translation.activate(lang)
        path = request.POST.get('next')
        if path == 'change_language':
            return redirect('movie:index')
        else:    
            return redirect(path)

#public views
def index(reauest):
    videos = cache.get('index_videos')
    if not videos:
        videos = Movie.objects.all()[:14]
        if videos:
            cache.set('index_videos', videos, 60 * 60)
    
    print(videos)
    serials = cache.get('index_serials')
    if not serials:
        serials = Serial.objects.all().order_by('-date')[:12]
        if serials:
            cache.set('index_serials', serials, 60 * 60)

    context = {
        'videosr':videos[:2],
        'videosf':videos[2:],
        'serials':serials
    }
    return render(reauest, 'publick/index.html', context)


def contact(request):
    if request.method == 'POST':
        form = FormContactForm(request.POST)
        if form.is_valid():
            cd  = form.cleaned_data
            ContactUs.objects.create(
                name = cd['name'], email=cd['email'],
                website = cd['website'], message = cd['message']
            )
            messages.success(request, _('your message with successfully registered '), 'success')
            return redirect('movie:contact')
        else:
            form = FormContactForm(request.POST)
            context = {
                'form':form,
            }
            messages.warning(request, _('please check fields for error'))
        return render(request, 'publick/contact.html', context)

    else:
        form = FormContactForm()
        context = {
            'form':form,
        }

        return render(request, 'publick/contact.html', context)


def collection(request):
    film_all = cache.get('collection_film_all')
    if not film_all:
        film_all = Movie.objects.all()
        if film_all:
            cache.set('collection_film_all',film_all, 60 * 15)
    
    serial_all = cache.get('collection_serial_all')
    if not serial_all:
        serial_all = Serial.objects.all()
        if serial_all:
            cache.set('collection_serial_all', serial_all, 60 * 15)

    if request.GET.get('type'):
        type = request.GET.get('type')
        film_all = film_all.filter(is_a=type)
        serial_all = serial_all.filter(is_a=type)
        all_list = list(chain(film_all,serial_all))

    elif request.GET.get('choice'):
        choice = request.GET.get('choice')
        film_all = film_all.filter(choice=choice)
        serial_all = serial_all.filter(choice=choice)
        all_list = list(chain(film_all,serial_all))
    
    elif request.GET.get('gener'):
       gener = request.GET.get('gener')
       film_all = film_all.filter(gener=gener) or film_all.filter(gener_en=gener)
       serial_all = serial_all.filter(gener=gener) or serial_all.filter(gener_en=gener)
       all_list = list(chain(film_all,serial_all))
    
    elif request.GET.get('date'):
       date = request.GET.get('date')
       film_all = film_all.filter(date__years=date)
       serial_all = serial_all.filter(date__years=date)
       all_list = list(chain(film_all,serial_all))
       
    else:
        all_list = cache.get('collection_all_list')
        if not all_list:
            film_ir = film_all.filter(choice='iranian')[:20]
            film_ha = film_all.filter(choice='halliwood')[:20]
            film_ba = film_all.filter(choice='balliwood')[:20]
            film_ar = film_all.filter(choice='arabic')[:20]
            film_an = film_all.filter(choice='animate')[:20]
            film_tu = film_all.filter(choice='turkish')[:20]
            film_chi = film_all.filter(choice='child')[:20]
            film_cha = film_all.filter(choice='chaina')[:20]

            serial_ir = serial_all.filter(choice='iranian')[:20]
            serial_ha = serial_all.filter(choice='halliwood')[:20]
            serial_ba = serial_all.filter(choice='balliwood')[:20]
            serial_ar = serial_all.filter(choice='arabic')[:20]
            serial_an = serial_all.filter(choice='animate')[:20]
            serial_tu = serial_all.filter(choice='turkish')[:20]
            serial_chi = serial_all.filter(choice='child')[:20]
            serial_cha = serial_all.filter(choice='chaina')[:20]

            all_list = list(chain(
                serial_ir, film_ir,serial_ha, film_ha,
                serial_ba, film_ba,serial_chi,film_chi,
                serial_an, film_an,serial_cha,film_cha,
                serial_tu, film_tu,serial_ar, film_ar,
            ))
            if all_list:
                cache.set('collection_all_list', all_list, 7200)
                
    print(all_list)
    page = request.GET.get('page', 1)

    paginator = Paginator(all_list, 20)

    try:
        searchs = paginator.page(page)
    except PageNotAnInteger:
        searchs = paginator.page(1)
    except EmptyPage:
        searchs = paginator.page(paginator.num_pages)

    context = {
        'searchs' : searchs,
        'choice':request.GET.get('choice'),
        'type':request.GET.get('type'),
        'date': request.GET.get('date'),
        'gener':request.GET.get('gener'),
    }
    return render(request, 'publick/collection.html', context)


def search(request):
    if request.GET.get('q'):
        query = request.GET.get('q')
        movies = Movie.objects.filter(
            Q(name__contains=query) | Q(date__contains=query) |
            Q(description__contains=query) | Q(description_en__contains=query) |
            Q(category__name__contains=query) | Q(name_en__contains=query) |
            Q(category__name_en__contains = query)
        )
        serials = Serial.objects.filter(
            Q(name__contains=query) | Q(date__contains=query) |
            Q(description__contains=query) | Q(description_en__contains=query) |
            Q(category__name__contains=query) |  Q(name_en__contains=query) |
            Q(category__name_en__contains = query)

        )
        search_list = list(chain(movies , serials))

    else: 
        movies =Movie.objects.all()
        serials = Serial.objects.all()

        if request.GET.get('name'):
            name = request.GET.get('name')
            movies = movies.filter(name=name) or movies.filter(name_en=name)
            serials = serials.filter(name=name) or serials.filter(name_en=name)
        
        if request.GET.get('type'):
            type = request.GET.get('type')
            movies = movies.filter(is_a=type)
            serials = serials.filter(is_a=type)

        if request.GET.get('choice'):
            choice = request.GET.get('choice')
            movies = movies.filter(choice=choice)
            serials = serials.filter(choice=choice)

        search_list = list(chain(movies, serials))
        print(search_list)

    page = request.GET.get('page', 1)

    paginator = Paginator(search_list, 12)

    try:
        searchs = paginator.page(page)
    except PageNotAnInteger:
        searchs = paginator.page(1)
    except EmptyPage:
        searchs = paginator.page(paginator.num_pages)

    context = {
        'searchs' : searchs,
        'choice':request.GET.get('choice'),
        'type':request.GET.get('type'),
        'name':request.GET.get('name'),
        'q':request.GET.get('q')
    }

    return render(request, 'publick/search.html', context)


#movie views
@login_required
def film(request, slug):
    video = cache.get(f'film_{slug}')
    if not video:
        video = Movie.objects.get(slug=slug)
        if video:
            cache.set(f'film_{slug}', video, 3600)
    save = video.save_movie.filter(user = request.user)

    context = {
        'video':video,
        'rating':video.ratin*10,
        'save': save
    }
    
    return render(request, 'publick/film_singel.html', context)


def about(request):
    return render(request, 'publick/about.html')


#serial views
@login_required
def serial(request, slug):
    video = cache.get(f'serial_{slug}')
    if not video:
        video = Serial.objects.get(slug=slug)
        if video:
            cache.set(f'serial_{slug}', video, 3600)

    save = video.save_serial.filter(user = request.user)
    context = {
        'video':video,
        'rating':video.ratin*10,
        'sessions':video.sessions_serial.all(),
        'save':save
    }
    
    return render(request, 'serial/serial.html', context)


@login_required
def session(request, slug):
    episod = get_object_or_404(SerialSession,slug=slug)
    serial_id = episod.serial.pk
    video = get_object_or_404(Serial,pk=serial_id)
    serials = episod.serial_session.all()

    context = {
        'video':video,
        'rating':video.ratin*10,
        'serials':serials,
        'episod':episod
    }
    return render(request, 'serial/session.html', context)


@login_required
def serial_single(request, slug):
    episod = cache.get(f'serial_single_{slug}')
    if not episod:
        episod = get_object_or_404(SerialFilms,slug=slug)
        if episod:
            cache.set(f'serial_single_{slug}',episod, 60 * 60)
    serial_id = episod.serial.pk
    video = get_object_or_404(Serial,pk=serial_id)
    serials = video.serial_film.all()

    context = {
        'video':video,
        'rating':video.ratin*10,
        'serials':serials,
        'episod':episod,
    }
    print(serials)
    return render(request, 'serial/serial_singel.html', context)


#review views
@login_required
def singel_review(request, slug):
    review = Review.objects.get(slug=slug)

    context = {
        'review':review,
    }

    return render(request, 'review/singel_review.html', context)



def review(request):
    review = cache.get('review')
    if not review:
        review = Review.objects.all()
        cache.set('review', review, 360)

    if request.GET.get('name'):
        name = request.GET.get('name')
        reviews = review.filter(name=name) or review.filter(name_en=name)

    if request.GET.get('type'):
        type = request.GET.get('type')
        review = review.filter(is_for = type)

    if request.GET.get('choice'):
        choice = request.GET.get('choice')
        review = review.filter(choice = choice)

    page = request.GET.get('page', 1)

    paginator = Paginator(review, 12)

    try:
        reviews = paginator.page(page)
    except PageNotAnInteger:
        reviews = paginator.page(1)
    except EmptyPage:
        reviews = paginator.page(paginator.num_pages)

    context = {
        'reviews' : reviews,
        'choice':request.GET.get('choice'),
        'type':request.GET.get('type'),
        'name':request.GET.get('name'),
        'q':request.GET.get('q')
    }

    return render(request, 'review/review.html', context)