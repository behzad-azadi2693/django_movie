from api.serializer_movie import MovieChoiceListSerializer
from django.contrib.contenttypes import fields
from accounts import models
from movie.models import Category, ContactUs, NewsLetters, MessagesSending, Save
from rest_framework.serializers import ModelSerializer

class NewsLettersSerializer(ModelSerializer):
    class Meta:
        model = NewsLetters
        fields = ('email',)

class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'name_en')


class ContactUsSerializer(ModelSerializer):
    class Meta:
        model = ContactUs
        fields = ('name','email','website','message')


class MessagesSendingSerializer(ModelSerializer):
    class Meta:
        model = MessagesSending
        fields = ('subject','messages')



class SaveSerializer(ModelSerializer):
    class Meta:
        model = Save
        fields = ('user','content_object')