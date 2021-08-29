from movie.models import Serial, SerialSession, SerialFilms
from rest_framework.reverse import reverse
from rest_framework.serializers import (
                HyperlinkedModelSerializer, ModelSerializer, SerializerMethodField
            )


class SerialTenListSerializer(HyperlinkedModelSerializer):
    serial_url_all = SerializerMethodField()
    serial_url = SerializerMethodField()
    class Meta:
        model = Serial
        fields = ['image', 'name', 'name_en', 'choice', 'is_a','serial_url_all','serial_url']

    def get_serial_url_all(self, obj):
        result = '{}'.format(reverse('api:serial_list', args=[obj.choice]),)
        return result

    def get_serial_url(self, obj):
        result = '{}'.format(reverse('api:serial_detail', args=[obj.slug]),)
        return result

class SerialChoceListSerializer(ModelSerializer):
    serial_url = SerializerMethodField()
    class Meta:
        model = Serial
        fields = ['image', 'name', 'name_en','serial_url']

    def get_serial_url(self, obj):
        result = '{}'.format(reverse('api:serial_detail', args=[obj.slug],))
        return result


class SerialAllListSerializer(ModelSerializer):
    serial_url = SerializerMethodField()
    class Meta:
        model = Serial
        fields = ['image', 'name', 'name_en', 'choice','serial_url']

    def get_serial_url(self, obj):
        result = '{}'.format(reverse('api:serial_detail', args=[obj.slug],))
        return result


class SerialSerializer(ModelSerializer):
    #edit_serial =    SerializerMethodField() #reverse('api:serial_edit',args=[video.slug]),
    #create_session = SerializerMethodField() #reverse('api:create_session',args=[video.slug])
    class Meta:
        model = Serial
        fields = ('image', 'name', 'name_en','title','description','description_en','gener','gener_en',
          'director','writer','stars','filmpas','awards','ratin','category','date','choice','time')

    #def get_edit_serial(self, obj):
    #    result = '{}'.format(reverse('api:serial_edit',args=[obj.slug]),)
    #    return result
#
    #def get_create_session(self, obj):
    #    result = '{}'.format(reverse('api:create_session',args=[obj.slug]),)
    #    return result


class AdminSerialFilmSerializer(ModelSerializer):
    edit_episod = SerializerMethodField()
    class Meta:
        model = SerialFilms
        fields = ('title','serial1080','serial720','serial480','edit_episod')

    def get_edit_episod(self, obj):
        result = '{}'.format(reverse('api:serial_film_edit', args=[obj.pk]))
        return result



class AdminSerialSessionSerializer(ModelSerializer):
    edit_session = SerializerMethodField()
    create_episod = SerializerMethodField()
    serial_session = AdminSerialFilmSerializer(many = True)

    class Meta:
        model = SerialSession
        fields = ('session','title','subtitle','serial_session','edit_session','create_episod')
        depth = 1

    def get_edit_session(self, obj):
        result = '{}'.format(reverse('api:session_edit', args=[obj.pk]))
        return result

    def get_create_episod(self, obj):
        result = '{}'.format(reverse('api:create_serial_film', args=[obj.pk,obj.serial.slug]))
        return result



class SerialFilmSerializer(ModelSerializer):
    class Meta:
        model = SerialFilms
        fields = ('title','serial1080','serial720','serial480')


class SerialSessionSerializer(ModelSerializer):
    serial_session = SerialFilmSerializer(many = True)
    class Meta:
        model = SerialSession
        fields = ('session','title','subtitle','serial_session')
        depth = 1


