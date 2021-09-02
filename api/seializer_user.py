from django.contrib.sessions.models import Session
from movie.models import HistoryPaid, SessionUser, Save, Movie
from accounts.models import User
from rest_framework import serializers
from rest_framework.reverse import reverse

class PhoneSerializer(serializers.Serializer):
    phone_number = serializers.IntegerField()


 
class OtpSerializer(serializers.Serializer):
    otp = serializers.IntegerField()




class KeySerializer(serializers.ModelSerializer):
    delete_session = serializers.SerializerMethodField()
    class Meta:
        model = Session()
        fields = ('session_key','delete_session')

    def get_delete_session(self, obj):
        result = '{}'.format(reverse('api:delete_session'))
        return result
        
class SessionSerializer(serializers.ModelSerializer):
    session_key = KeySerializer()
    class Meta:
        model = SessionUser()
        fields = ('session_key', 'device', 'os', 'date_joiin', 'ip_device')


class PaidSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoryPaid()
        fields = ('date' ,'price' ,'code')

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('phone_number',)




class RelatedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('name','image')


class SaveSerializer(serializers.ModelSerializer):
    content_object = RelatedSerializer()
    url = serializers.SerializerMethodField()

    class Meta:
        model = Save
        fields = ('content_object','url')

    def get_url(self, obj):
        if obj.content_object.is_a == 'movie':
            result = '{}'.format(reverse('api:movie_detail',args = [obj.content_object.slug]))
            return result

        if obj.content_object.is_a == 'serial':
            result = '{}'.format(reverse('api:serial_detail',args = [obj.content_object.slug]))
            return result