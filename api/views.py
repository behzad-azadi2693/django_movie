from django.contrib import messages
from rest_framework import response, serializers
from movie.models import NewsLetters
from rest_framework.response import Response
from .serializer_serial import SerialTenListSerializer
from .serializer_movie import MovieTenListSerializer
from rest_framework.decorators import api_view
from movie.models import Movie,Serial, Save
from rest_framework import status
from .serializer import CategorySerializer, ContactUsSerializer, MessagesSendingSerializer,NewsLettersSerializer
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache


@api_view(['GET'],)
def index(request):
    
    video = cache.get('collection_film_all')
    if not video:
        video = Movie.objects.all()
        if video:
            cache.set('collection_film_all', video, 60*60)
    
    serial = cache.get('collection_serial_all')
    if not serial:
        serial = Serial.objects.all()
        if serial:
            cache.set('collection_serial_all', serial, 60 * 60)

    m_iranian = MovieTenListSerializer(video.filter(choice='iranian')[:10], many=True).data
    s_iranian = SerialTenListSerializer(serial.filter(choice='iranian')[:10], many=True).data   
    m_halliwod = MovieTenListSerializer(video.filter(choice='halliwood')[:10], many=True).data
    s_halliwod = SerialTenListSerializer(serial.filter(choice='halliwood')[:10], many=True).data    
    m_balliwod = MovieTenListSerializer(video.filter(choice='balliwood')[:10], many=True).data
    s_balliwod = SerialTenListSerializer(serial.filter(choice='balliwood')[:10], many=True).data    
    m_turkish = MovieTenListSerializer(video.filter(choice='turkish')[:10], many=True).data
    s_turkish = SerialTenListSerializer(serial.filter(choice='turkish')[:10], many=True).data   
    m_arabian = MovieTenListSerializer(video.filter(choice='arabic')[:10], many=True).data
    s_arabian = SerialTenListSerializer(serial.filter(choice='arabic')[:10], many=True).data    
    m_chaina = MovieTenListSerializer(video.filter(choice='chaina')[:10], many=True).data
    s_chaina = SerialTenListSerializer(serial.filter(choice='chaina')[:10], many=True).data 
    m_child = MovieTenListSerializer(video.filter(choice='child')[:10], many=True).data
    s_child = SerialTenListSerializer(serial.filter(choice='child')[:10], many=True).data   
    m_animate = MovieTenListSerializer(video.filter(choice='animate')[:10], many=True).data
    s_animate = SerialTenListSerializer(serial.filter(choice='animate')[:10], many=True).data   
    srz = (s_animate,s_arabian,s_balliwod,s_chaina,s_child,s_halliwod,s_iranian,s_turkish,
           m_animate,m_arabian,m_balliwod,m_chaina,m_child,m_halliwod,m_iranian,m_turkish)
    
    return Response(srz, status=status.HTTP_200_OK)


@api_view(["GET", 'POST'])
def category_create(request):
    if request.method == "POST":
        form = CategorySerializer(data=request.data)
        if form.is_valid():
            form.save()
            return Response(form.data, status=status.HTTP_201_CREATED)
        else:
            return Response(form.data, status=status.HTTP_400_BAD_REQUEST)
    else:
        form = CategorySerializer()
        return Response(form.data)


@api_view(['GET'],)
def admin_controller(request):
    if request.user.is_admin:
        create_movie = reverse('api:movie_create')
        create_serial = reverse('api:serial_create')
        create_category = reverse('api:category_create')
        return Response((create_category,create_movie, create_serial), status=status.HTTP_200_OK)


@api_view(['GET','POST'])
def submit_email(request):
    if request.method == 'POST':
        form = NewsLettersSerializer(data=request.data)

        if form.is_valid():
            form.save()
            return response(form.data, status=status.HTTP_201_CREATEDTT)
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        form = NewsLettersSerializer()
        return Response(form.data)

@api_view(['GET','POST'])
def contact_us(request):
    if request.method == 'POST':
        form = ContactUsSerializer(data=request.data)
        if form.is_valid():
            form.save()
            return Response(form.data, status=status.HTTP_201_CREATED)
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        form = ContactUsSerializer()
        return Response(form.data)


@api_view(['GET','POST'])
def send_email(request):
    if request.method == 'POST':
        form = MessagesSendingSerializer(data=request.data)

        if form.is_valid():
            form.save()
            email_all = NewsLetters.objects.all()
            email_list = []
            for email in email_all:
                email_list.append(email.email)
            try:
                send_mail(
                    form.subject,
                    form.message, 
                    'FILM-View Site',
                    email_list,
                    fail_silently=False,
                )
                return Response(form.data, status=status.HTTP_200_OK)
            except:
                message = 'dont send email'
            return Response(form.data, status=status.HTTP_201_CREATED)

        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

    else:
        form = MessagesSendingSerializer()
        return Response(form.data)

@api_view(['GET'],)
def save_serial(request, slug):
    try:
        video = Serial.objects.get(slug=slug)
    except Serial.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    save = video.save_serial.filter(user = request.user)

    if save:
        content_type = ContentType.objects.get_for_model(video)
        serial_del = Save.objects.get(user = request.user, content_type = content_type, object_id = video.pk)
        serial_del.delete()

    else:
        market = Save(
            user = request.user, content_object = video
        )
        market.save()

    return Response(status=status.HTTP_201_CREATED)


@api_view(['GET'],)
def save_movie(request, slug):
    try:
        video = Movie.objects.get(slug=slug)
    except Movie.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    save = video.save_movie.filter(user = request.user)

    if save:
        content_type = ContentType.objects.get_for_model(video)
        save_del = Save.objects.get(user = request.user, content_type = content_type, object_id = video.pk)
        save_del.delete()

    else:
        market = Save(
            user = request.user, content_object = video
        )
        market.save()

    return Response(status=status.HTTP_201_CREATED)