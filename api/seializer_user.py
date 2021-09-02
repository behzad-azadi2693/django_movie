from django.contrib.sessions.models import Session
from movie.models import HistoryPaid, SessionUser
from django.contrib.contenttypes import fields
from accounts import models
from rest_framework.fields import ModelField
from accounts.views import phone
from rest_framework import serializers


class PhoneSerializer(serializers.Serializer):
    phone_number = serializers.IntegerField()


 
class OtpSerializer(serializers.Serializer):
    otp = serializers.IntegerField()




class KeySerializer(serializers.ModelSerializer):
    class Meta:
        model = Session()
        fields = ('session_key',)
        
class SessionSerializer(serializers.ModelSerializer):
    session_key = KeySerializer()
    class Meta:
        model = SessionUser()
        fields = ('session_key', 'device', 'os', 'date_joiin')


class PaidSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoryPaid()
        fields = ('date' ,'price' ,'code')

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = ('phone_number',)