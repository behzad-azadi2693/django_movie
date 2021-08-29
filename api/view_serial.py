from os import stat
from rest_framework.response import Response
from movie.models import Serial, SerialFilms, SerialSession
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from django.urls import reverse
from .serializer_serial import (
                        SerialFilmSerializer, SerialAllListSerializer, SerialChoceListSerializer,SerialSerializer,
                        SerialSessionSerializer,AdminSerialSessionSerializer,
                    )


@api_view(['GET'])
def serial_list(request, choice):
    paginatore = PageNumberPagination()
    paginatore.page_size = 12

    video = Serial.objects.filter(choice = choice)

    result_page = paginatore.paginate_queryset(video, request)

    srz = SerialChoceListSerializer(result_page, many=True).data

    return paginatore.get_paginated_response(srz)


@api_view(['GET'],)
def serial_detail(request, slug):
    try:
        video = Serial.objects.get(slug=slug)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    srz_detail = SerialSerializer(video).data

    if not request.user.is_authenticated:
        srz_session = {'please loggin to account'}
    elif request.user.is_paid == True or request.user.is_admin:
        session = video.sessions_serial.all().order_by('id')
        if not request.user.is_admin:
            srz_session = SerialSessionSerializer(session, many=True).data
        if  request.user.is_admin:
            srz_session = AdminSerialSessionSerializer(session, many=True).data
            link = {
                    'edit_serial' : reverse('api:serial_edit',args=[video.slug]),
                    'create_session' : reverse('api:create_session',args=[video.slug])
                }

    else:
        ser_session = {'Please proceed to purchase a subscription'}

    link = {
        'edit_serial' : reverse('api:serial_edit',args=[video.slug]),
        'create_session' : reverse('api:create_session',args=[video.slug])
    }
    srz = (srz_detail, link)
    return Response(srz, status=status.HTTP_200_OK)


@api_view(['GET'])
def serial_all_list(request):
    paginator = PageNumberPagination()
    paginator.page_size = 12

    video = Serial.objects.all()

    result_page = paginator.paginate_queryset(video, request)

    srz= SerialAllListSerializer(result_page, many=True).data

    return paginator.get_paginated_response(srz)


@api_view(['GET','POST'])
def create_serial(request):
    if request.method == 'POST':
        form = SerialSerializer(data=request.data)
        if form.is_valid():
            form.save()
            return Response(form.data, status=status.HTTP_201_CREATED)
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        form = SerialSerializer()
        return Response(form.data)



@api_view(['GET','PUT'])
def edit_serial(request, slug):
    try:
        video = Serial.objects.get(slug=slug)
    except Serial.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        form = SerialSerializer(video, data=request.data)
        if form.is_valid():
            form.save()
            return Response(form.data, status=status.HTTP_201_CREATED)
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        form = SerialSerializer(video)
        return Response(form.data)



@api_view(['GET','POST'])
def create_session(request, slug):
    try:
        video = Serial.objects.get(slug=slug)
    except Serial.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    video_data = Serial(serial = video)

    if request.method == 'POST':
        form = SerialSessionSerializer(video_data, request.data)
        if form.is_valid():
            form.save()
            return Response(form.data, status=status.HTTP_201_CREATED)
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        form = SerialSessionSerializer(video_data)
        return Response(form.data)


@api_view(['GET','PUT'])
def edit_session(request, pk):
    try:
        sesn = SerialSession.objects.get(pk=pk)
    except Serial.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        form = SerialSessionSerializer(request.data)
        if form.is_valid():
            form.save()
            return Response(form.data, status=status.HTTP_201_CREATED)
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        form = SerialSessionSerializer(sesn)
        return Response(form.data)


@api_view(['GET','POST'])
def create_serial_film(request, pk, slug):
    try:
        sesn = SerialSession.objects.get(pk=pk)
        video = Serial.objects.get(slug=slug)
    except SerialSession.DoesNotExist or Serial.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    video_data = SerialFilms(session=sesn, serial=video)

    if request.method == 'POST':
        form = SerialFilmSerializer(video_data, data=request.data)
        if form.is_valid():
            form.save()
            return Response(form.data, status=status.HTTP_201_CREATED)
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        form = SerialFilmSerializer(video_data)
        return Response(form.data)


@api_view(['GET','PUT'])
def edit_serial_film(request, pk):
    try:
        video = SerialFilms.objects.get(pk=pk)
    except SerialSession.DoesNotExist or Serial.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'PUT':
        form = SerialFilmSerializer(video, data=request.data)
        if form.is_valid():
            form.save()
            return Response(form.data, status=status.HTTP_201_CREATED)
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        form = SerialFilmSerializer(video)
        return Response(form.data)