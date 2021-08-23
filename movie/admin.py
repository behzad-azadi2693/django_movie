from django.contrib import admin
from django.utils.html import mark_safe
from django.contrib.sessions.models import Session
from django.utils.translation import gettext_lazy as _
from .models import (
                Category, ContactUs, Movie,
                Save, Serial, SerialFilms, User,
                SerialSession, Review, SessionUser, 
                HistoryPaid, NewsLetters, MessagesSending
            )


@admin.register(Movie)
class AdminMovie(admin.ModelAdmin):
    date_hierarchy = 'date'
    prepopulated_fields = {'slug': ('title', )}
    list_filter = ('title','name', 'name_en','slug', 'gener','date', 'ratin')
    list_display = ('name', 'name_en','title', 'slug', 'gener', 'choice', 'awatar')
    search_fields = ('name', 'name_en','title', 'slug', 'director')
    fieldsets = (
        (_('Information'), {'fields':('name','name_en', 'title', 'slug', 'gener', 'gener_en')}),
        (_('Description'),{'fields':('description', 'description_en')}),
        (_('Data'),{'fields':('awatar','image','filmpas','film1080','filme720','film480','subtitle')}),
        (_('Information Movie'),{'fields':('date', 'ratin', 'awards', 'time', 'choice', 'category')}),
        (_('Human Factor'),{'fields':('director', 'writer', 'stars')})
    )
    
    def awatar(self, obj):
        return mark_safe('<img src="{url}" width="50" height="50" />'.format(url=obj.image.url,))
        
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_add_permission(self, request, obj=None):
        return False


@admin.register(ContactUs)
class AdminContactUs(admin.ModelAdmin):
    list_display = ('name','email','website')
    list_filter =('name','email', 'website')
    search_fields = ('name', 'email', 'website')
    fieldsets = (
        (_('Information'),{'fields':('name','email','website')}),
        (_('Message'),{'fields':('message',)}),
    )
        
    def has_add_permission(self, request, obj=None):
        return False


@admin.register(SerialFilms)
class AdminSerialFilm(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title', )}
    list_filter = ('episod','title','slug')
    list_display = ('episod','title','slug')
    search_fields = ('episod','title','slug')
    fieldsets = (
        (_('Information'),{'fields':('episod','title','slug', 'session', 'serial')}),
        (_('Data'),{'fields':('serial1080','serial720','serial480')}),
    )

    def has_change_permission(self, request, obj=None):
        return False
    
    def has_add_permission(self, request, obj=None):
        return False


@admin.register(SerialSession)
class AdminSerialSession(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title', )}
    list_filter = ('title', 'slug', 'session')
    list_display = ('title','slug', 'session')
    search_fields = ('title', 'slug', 'session')
    fieldsets = (
        (_('Information'), {'fields':('title', 'slug', 'session')}),
        (_('Data'),{'fields':( 'subtitle',)}),
    )

    
    def awatar(self, obj):
        return mark_safe('<img src="{url}" width="50" height="50" />'.format(url=obj.image.url,))

    def has_change_permission(self, request, obj=None):
        return False
        
    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Serial)
class AdminSerial(admin.ModelAdmin):
    date_hierarchy = 'date'
    prepopulated_fields = {'slug': ('title', )}
    list_filter = ('title','name', 'name_en','slug', 'gener','date', 'ratin')
    list_display = ('id','name', 'name_en','title', 'slug', 'gener', 'gener_en', 'awatar')
    search_fields = ('name', 'name_en','title', 'slug', 'director')
    fieldsets = (
        (_('Information'), {'fields':('name', 'name_en', 'title', 'slug', 'gener', 'gener_en')}),
        (_('Description'),{'fields':('description', 'description_en')}),
        (_('Data'),{'fields':( 'image', 'filmpas')}),
        (_('Information Movie'),{'fields':('date', 'ratin', 'awards', 'time', 'choice', 'category')}),
        (_('Human Factor'),{'fields':('director', 'writer', 'stars')})
    )
    
    def awatar(self, obj):
        return mark_safe('<img src="{url}" width="50" height="50" />'.format(url=obj.image.url,))

    def has_change_permission(self, request, obj=None):
        return False
        
    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Review)
class AdminReview(admin.ModelAdmin):
    prepopulated_fields = {'slug':('title',)}
    list_display = ('name','name_en','title','slug', 'id','is_for','choice', 'awatar')
    list_filter = ('name','name_en','title', 'slug', 'id','is_for', 'choice')
    fieldsets = (
        (_('Information'),{'fields':('name','name_en','title','slug','description','description_en','choice','filmpas')}),
        (_('Generic'),{'fields':('content_type','object_id','is_for')})
    )   
    def awatar(self, obj):
        return mark_safe('<img src="{url}" width="50" height="50" />'.format(url=obj.content_object.image.url,))

    def has_change_permission(self, request, obj=None):
        return False
        
    def has_add_permission(self, request, obj=None):
        return False


@admin.register(SessionUser)
class AdminSessionUser(admin.ModelAdmin):
    list_filter = ('user','id', 'date_joiin')
    list_display = ('user','session_key', 'date_joiin')
    
    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False    

@admin.register(Save)
class AdminSave(admin.ModelAdmin):
    list_display=('user_saved','user','awatar',)
    list_filter = ('user',)

    def user_saved(self,obj):
        return f'{obj.user} saved {obj.content_object.name}'

    def awatar(self, obj):
        return mark_safe('<img src="{url}" width="50" height="50" />'.format(url=obj.content_object.image.url,))
    
    def has_change_permission(self, request, obj=None):
        return False
        
    def has_add_permission(self, request, obj=None):
        return False


@admin.register(HistoryPaid)
class AdminPaid(admin.ModelAdmin):
    date_hierarchy = 'date'
    list_display = ('date','user', 'code')
    filter = ('user', 'date')


@admin.register(MessagesSending)
class AdminMessageSending(admin.ModelAdmin):
    date_hierarchy = 'date'
    list_display = ('date','subject')
    list_filter = ('date', 'subject')


admin.site.register(Category)


admin.site.register(NewsLetters)


admin.site.register(Session)
