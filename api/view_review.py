from django.db import models
from django.urls.base import reverse
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.response import Response
from movie.models import Movie, Review, Serial
from rest_framework.decorators import api_view
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from .serializer_review import (
                    CreateReviewMovieSerializer, CreateReviewSerialSerializer, ReviewMovieSerializer, ReviewSerialSerializer,
                    ReviewMovieDetailSerializer,ReviewMovieDetailSerializer,ReviewSerialDetailSerializer,EditReviewSerializer,
                    ReviewSerializer
                )



@api_view(['GET'])
def review_list(request):
    paginator = PageNumberPagination()
    paginator.page_size = 12
    
    movie = Review.objects.filter(is_for='movie')
    srz_movie = ReviewMovieSerializer(movie, many=True).data
    serial = Review.objects.filter(is_for='serial')
    srz_serial = ReviewSerialSerializer(serial, many=True).data

    srz_all = srz_movie + srz_serial

    result_page = paginator.paginate_queryset(srz_all ,request)

    srz = result_page

    return paginator.get_paginated_response(srz)



@api_view(['GET','POST'])
def create_review_movie(request, pk):
    if not (request.user.is_authenticated and request.user.is_admin):
        return redirect('api:index')

    try:
        video = Movie.objects.get(pk=pk)
    except Movie.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    video_post = Review(name=video.name, name_en=video.name_en,is_for='movie',choice=video.choice,content_object=video) 

    if request.method == 'POST':
        form = CreateReviewMovieSerializer(video_post, data=request.data)
        if form.is_valid():
            form.save()
            return Response('review created ok', status=status.HTTP_201_CREATED)
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        form = CreateReviewMovieSerializer()
        return Response(form.data)



@api_view(['GET','POST'])
def create_review_serial(request, pk):
    if not (request.user.is_authenticated and request.user.is_admin):
        return redirect('api:index')

    try:
        video = Serial.objects.get(pk=pk)
    except Movie.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    video_post = Review(name=video.name, name_en=video.name_en,is_for='serial',choice=video.choice,content_object=video) 

    if request.method == 'POST':
        form = CreateReviewSerialSerializer(video_post, data=request.data)
        if form.is_valid():
            form.save()
            return Response('review created ok', status=status.HTTP_201_CREATED)
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        form = CreateReviewSerialSerializer()
        return Response(form.data)


@api_view(['GET'])
def review_movie_detail(request, slug):
    try:
        video = Review.objects.get(slug = slug, is_for = 'movie')
    except Review.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    srz_detail = ReviewSerializer(video).data

    link = None
    if not request.user.is_authenticated:
        srz_data = {'please login to account'}
    if request.user.is_paid or request.user.is_admin:
        srz_date = ReviewMovieDetailSerializer(video).data
        if request.user.is_admin:
            link = {
                'edit_review': reverse('api:edit_review', args=[video.slug])
            }
    else:
        srz_data = {'Please proceed to purchase a subscription'}
    form = (srz_data, srz_detail, link )
    return Response(form, status=status.HTTP_200_OK)


@api_view(["GET"])
def review_serial_detail(request, slug):
        try:
            video = Review.objects.get(slug = slug, is_for = 'serial')
        except Review.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        link = None 
        srz_detail = ReviewSerializer(video).data
        if not request.user.is_authenticated:
            srz_data = {'please login to account'}
        elif request.user.is_paid or request.user.is_admin:
            srz_date = ReviewSerialDetailSerializer(video).data
            if request.user.is_admin:
                link = {
                    'edit_review': reverse('api:edit_review', args=[video.slug])
                }
                
        else:
            srz_data = {'Please proceed to purchase a subscription'}
        form = (srz_data, srz_detail, link )
        return Response(form, status=status.HTTP_200_OK)



@api_view(['GET','PUT'])
def edit_review(request, slug):
    if not (request.user.is_authenticated and request.user.is_admin):
        return redirect('api:index')
        
    try:
        video = Review.objects.get(slug=slug)
    except Review.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        form = EditReviewSerializer(video, data=request.data)
        if form.is_valid():
            form.save()
            return Response(form.data, status=status.HTTP_201_CREATED)
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
    
    else:
        form = EditReviewSerializer(video)
        return Response(form.data)
