
from .models import Serial, Movie, Save, User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404


@login_required
def user(request):
    pk = request.user.pk
    user = get_object_or_404(User, pk=pk)
    saves = Save.objects.filter(user = request.user)

    context = {
        'user':user,
        'ip':request.META['REMOTE_ADDR'],
        'info':request.META['HTTP_USER_AGENT'],
        'saves':saves,
    }

    return render(request, 'publick/user.html', context)

@login_required
def save_serial(request, slug):
    serial = Serial.objects.get(slug=slug)
    save = serial.save_serial.filter(user = request.user)

    if save:
        content_type = ContentType.objects.get_for_model(serial)
        serial_del = Save.objects.get(user = request.user, content_type = content_type, conten_id = serial.pk)
        serial_del.delete()

    else:
        market = Save(
            user = request.user, content_object = serial
        )
        market.save()

    return redirect(serial)


from django.contrib.contenttypes.models import ContentType

@login_required
def save_movie(request, slug):
    movie = Movie.objects.get(slug=slug)
    save = movie.save_movie.filter(user = request.user)

    if save:
        content_type = ContentType.objects.get_for_model(movie)
        save_del = Save.objects.get(user = request.user, content_type = content_type, object_id = movie.pk)
        save_del.delete()

    else:
        market = Save(
            user = request.user, content_object = movie
        )
        market.save()

    return redirect(movie)
