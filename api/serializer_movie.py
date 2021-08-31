from copy import error
from django.contrib.contenttypes import fields
from django.db import models
from rest_framework import serializers
from movie.models import Movie, Save
from django.utils.translation import gettext_lazy as _
from rest_framework.serializers import (
    HyperlinkedModelSerializer, ModelSerializer, SerializerMethodField
)
from rest_framework.reverse import reverse


class MovieTenListSerializer(HyperlinkedModelSerializer):
    movie_url_all = SerializerMethodField()
    movie_url = SerializerMethodField()
    class Meta:
        model = Movie
        fields = ['image','name', 'name_en', 'is_a','choice', 'movie_url','movie_url_all']

    def get_movie_url_all(self, obj):
        result = '{}'.format(reverse('api:movie_list', args=[obj.choice]),)
        return result

    def get_movie_url(self, obj):
        result = '{}'.format(reverse('api:movie_detail', args=[obj.slug]),)
        return result


class MovieChoiceListSerializer(ModelSerializer):
    movie_url = SerializerMethodField()
    class Meta:
        model = Movie
        fields = ['image', 'title', 'name', 'name_en', 'choice', 'is_a','movie_url']

    def get_movie_url(self, obj):
        result = '{}'.format(reverse('api:movie_detail', args=[obj.slug],),)
        return result

class MovieAllListSerializer(HyperlinkedModelSerializer):
    movie_url = SerializerMethodField()
    class Meta:
        model = Movie
        fields = ['image','name', 'name_en', 'choice','movie_url']
    
    def get_movie_url(self, obj):
        result = '{}'.format(reverse('api:movie_detail', args=[obj.slug],),)
        return result


class MovieDetailDataSerializer(ModelSerializer):
    class Meta:
        model = Movie
        fields = ('film1080','filme720','film480','subtitle')


class MovieSerializer(ModelSerializer):       
    class Meta:
        model = Movie
        fields = ('image', 'name', 'name_en','title','description','description_en','gener','gener_en','subtitle','choice',
                  'director','writer','stars','filmpas','awards','ratin','category','time','date','film1080','filme720','film480')
