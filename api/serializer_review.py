from os import read
from django.forms import fields, models
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer
from movie.models import Review, Movie, Serial
from .serializer_movie import MovieSerializer
from .serializer_serial import SerialSerializer
from rest_framework.reverse import reverse


class ReviewMovieDetailSerializer(ModelSerializer):
    content_object =  MovieSerializer()
    class Meta:
        model = Review
        fields = ('name','name_en','title','description','description_en','is_for','filmpas','content_object','choice')


class ReviewSerialDetailSerializer(ModelSerializer):
    content_object =  MovieSerializer()
    class Meta:
        model = Review
        fields = ('name','name_en','title','description','description_en','is_for','filmpas','content_object','choice')


class CreateReviewMovieSerializer(ModelSerializer):
    class Meta:
        model = Review
        fields = ('name','name_en','title','description','description_en','is_for','filmpas','content_object','choice')

        extra_kwargs = {
            'name':{'read_only':True},
            'name_en':{'read_only':True},
            'is_for':{'read_only':True},
            'choice':{'read_only':True},
            'content_object':{'read_only':True},
        }


class CreateReviewSerialSerializer(ModelSerializer):
    class Meta:
        model = Review
        fields = ('name','name_en','title','description','description_en','is_for','filmpas','choice','content_object')

        extra_kwargs = {
            'name':{'read_only':True},
            'name_en':{'read_only':True},
            'is_for':{'read_only':True},
            'choice':{'read_only':True},
            'content_object':{'read_only':True},
        }


class EditReviewSerializer(MovieSerializer):
    class Meta:
        model = Review
        fields = ('name','name_en','title','description','description_en','filmpas')


class ImageMovie(MovieSerializer):
    class Meta:
        model = Movie
        fields = ('image',)


class ReviewMovieSerializer(ModelSerializer):
    content_object = ImageMovie()
    review_url = SerializerMethodField()
    class Meta:
        model = Review
        fields = ('name','name_en','description','description_en','content_object', 'review_url')

    def get_review_url(self, obj):
        result = '{}'.format(reverse('api:review_movie_detail', args=[obj.slug]))
        return result

class ImageSerial(MovieSerializer):
    class Meta:
        model = Serial
        fields = ('image',)

class ReviewSerialSerializer(ModelSerializer):
    content_object = ImageSerial()
    review_url = SerializerMethodField()
    class Meta:
        model = Review
        fields = ('name','name_en','description','description_en','content_object','review_url')

    def get_review_url(self, obj):
        result = '{}'.format(reverse('api:review_serial_detail', args=[obj.slug]))