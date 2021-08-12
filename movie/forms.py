from collections import namedtuple
from django import forms
from django.contrib.messages.api import error
from django.db.models import fields
from django.contrib.auth import models
from django.db.models import query
from django.db.models.query import QuerySet
from django.forms import widgets
from django.http import request
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import Category, User, Movie, Serial, SerialFilms, SerialSession, Review


class UserCreationForm(forms.ModelForm):
    password = forms.CharField(label='password', widget=forms.PasswordInput)
    password_confierm = forms.CharField(label='password', widget=forms.PasswordInput)

    class Meta:
        models = User
        fields = ('phone_number', 'date_paid')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] and cd['password_confirm'] and cd['password'] != cd['password_confirm']:
            raise forms.ValidationError(_("password and confirm password must be match "))

        return cd['password_confirm']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()
    class Meta:
        models = User
        fields = ('phone_number', 'date_paid', 'password')

    def clean_password(self):
        return self.initial['password']


messages = {
    'required':_("this field is required"),
    'invalid':_("It is not correct"),
    'max_length':_("The size of the characters is large of 15 character"),
    'min_length':_("The size of the characters is small of 9 character"),
    'max_value':_("out of range maximum size"),
    'min_value':_("out of range minimum size"),
}
CHOICES =(
    ("iranian", "iranian"),
    ("halliwood", "halliwood"),
    ("balliwood", "balliwood"),
    ("arabic", "arabic"),
    ("chaina", "chaina"),
)


class UserPhoneForm(forms.Form):
    phone_number = forms.CharField(
        label=_("Password sent"),
        error_messages=messages,
        required=True,
        help_text=_("enter your phone number 09210000000..."),        
        widget=forms.TextInput(attrs={'placeholder':_("phone number ..."), 'class':'name', 'type':'number', 'value':None})
    )


class PasswordSms(forms.Form):
    password = forms.CharField(
        label=_("Password sent"),
        error_messages=messages,
        required=True,
        help_text=_("please neter password sent to you ... "),        
        widget=forms.TextInput(attrs={'placeholder':_("password sent ..."), 'class':'email', 'type':'number', 'value':None})
    )




class FormMovie(forms.ModelForm):
    ratin = forms.IntegerField(
        max_value=10,
        min_value=0,
        label=_('movie ratin'),
        required=False,
        error_messages=messages,
        help_text=_('input range of beetwean of 0-10')
    )
    class Meta:
        model = Movie
        fields = (
            'name', 'name_en','title','gener','gener_en','description','description_en',
            'director','writer','stars','time','date','awards','choice','category',
            'ratin','image','filmpas','film1080','filme720','film480','subtitle','slug'
        )
        widgets ={
            'slug':forms.HiddenInput(attrs={'readonly':'readonly','hidden':'hidden','value':'title'}),
        }
        labels = {
            'name':_('*movie name'),'slug':'','title':_('*movie title'),'description':_('*movie description'),'description_en':_('*movie description en'),
            'director':_('movie director'),'writer':_('movie writer'),'stars':_('movie stars'),'time':_('movie time'),'date':_('*movie date'),
            'awards':_('movie awards'),'choice':_('movie is'),'category':_('*movie category'),'ratin':_('movie ratin'),'name_en':_('*movie name en'),
            'image':_('*movie image'),'filmpas':_('*movie preview'),'film1080':_('movie quality 1080'),'filme720':_('movie quality 720'),
            'film480':_('movie quality 480'),'subtitle':_('movie subtitle'),'gener':_('*movie gener'),'gener_en':_('*movie gener en')
        }
        help_texts = {
            'ratin':_('this field get range of 0-10'),
            'date':_('this field get 2/10/2020'),
            'time':_('this field get 03:36:52'),
        }
        error_messages = {
            'name':{'required':_('this is fields required'),'max_length':_("this is field maximum character is 200")},
            'name_en':{'required':_('this is fields required'),'max_length':_("this is field maximum character is 200")},
            'gener':{'required':_('this is fields required'),'max_length':_("this is field maximum character is 200")},
            'gener_en':{'required':_('this is fields required'),'max_length':_("this is field maximum character is 200")},
            'title':{'required':_('this is fields required'),'max_length':_("this is field maximum character is 200")},
            'description':{'required':_('this is fields required'),},
            'description_en':{'required':_('this is fields required'),},
            'date':{'required':_('this is fields required'),},
            'choice':{'required':_('this is fields required'),},
            'category':{'required':_('this is fields required'),},
            'image':{'required':_('this is fields required'),},
        }


class FormSerial(forms.ModelForm):
    ratin = forms.IntegerField(
        max_value=10,
        min_value=0,
        label=_('movie ratin'),
        required=False,
        error_messages=messages,
        help_text=_('input range of beetwean of 0-10')
    )
    class Meta:
        model = Serial
        fields = (
            'name', 'name_en','title','gener','gener_en','description','description_en','date','time','awards','ratin',
            'director','writer','stars','choice','category','image','filmpas','slug'
            )
        exclude = ('is_serial',)
        widgets ={
            'slug':forms.HiddenInput(attrs={'readonly':'readonly','hidden':'hidden','value':'title'}),
        }
        labels = {
            'name':_('*serial name'),'name_en':_('*serial name en'),'gener':_('*serial gener'),'gener_en':_('*serial gener en'),'title':_('*serial title'),
            'description':_('*serial description'),'description_en':_('*serial description en'),'director':_('serial director'),
            'writer':_('serial writer'),'stars':_('serial stars'),'time':_('serial time'),'date':_('*serial date'),
            'awards':_('serial awards'),'choice':_('*serial choice'),'category':_('*serial category'),'ratin':_('serial ratin'),
            'image':_('*serial image'),'filmpas':_('*serial preview'),'slug':''
        }
        help_texts = {
            'ratin':_('this field get range of 0-10'),
            'time':_('this field get 03:36:52'),
            'date':_('this field get 2/10/2020'),
        }
        error_messages = {
            'name':{'required':_('this is fields required'),'max_length':_("this is field maximum character is 200")},
            'name_en':{'required':_('this is fields required'),'max_length':_("this is field maximum character is 200")},
            'title':{'required':_('this is fields required'),'max_length':_("this is field maximum character is 200")},
            'description':{'required':_('this is fields required'),},
            'description_en':{'required':_('this is fields required'),},
            'date':{'required':_('this is fields required'),},
            'category':{'required':_('this is fields required'),},
            'choice':{'required':_('this is fields required'),},
        }
class FormSerialFilm(forms.ModelForm):
    class Meta:
        model = SerialFilms
        fields = ('episod', 'title','serial','session','serial1080','serial720','serial480','slug')
        widgets ={
            'slug':forms.HiddenInput(attrs={'readonly':'readonly','hidden':'hidden','value':'title'}),
        }
        labels = {
            'episod':_('*movie episod'),'title':_('*movie title'),'session':_('*serial session'),'serial':_('*serial related'),
            'serial1080':_('serial quality 1080'),'serial720':_('serial quality 720'),'serial480':_('serial quality 480'),'slug':''
        }
        help_text = {
            'episod':_('tish field like 01')
        }
        error_messages = {
            'episod':{'required':_('this is fields required')},
            'title':{'required':_('this is fields required'),'max_length':_("this is field maximum character is 200")},
            'serial':{'required':_('this is fields required'),},
            'session':{'required':_('this is fields required'),},
        }


class FormSerialSession(forms.ModelForm):
    class Meta:
        model = SerialSession
        fields = ('title','serial','session','subtitle','slug')
        widgets ={
            'slug':forms.HiddenInput(attrs={'readonly':'readonly','hidden':'hidden','value':'title'}),
        }
        labels = {
            'title':_('*movie title'),'session':_('*serial session'),'serial':_('*serial related'),
            'subtitle':_('serial subtitle'),'slug':''
        }
        error_messages = {
            'title':{'required':_('this is fields required'),'max_length':_("this is field maximum character is 200")},
            'serial':{'required':_('this is fields required'),},
            'session':{'required':_('this is fields required'),},
        }


class FormCategory(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name','name_en')
        labels = {
            'name':_('*category name'),'name_en':_('*category name'),
        }
        error_messages = {
            'name':{'required':_('this is fields required'),'max_length':_("this is field maximum character is 200")},
            'name_en':{'required':_('this is fields required'),'max_length':_("this is field maximum character is 200")},

        }

class FormReview(forms.ModelForm):
    pk = forms.IntegerField(
        widget = forms.TextInput(),
        min_value=1,
        label=''
    )
    class Meta:
        model = Review
        fields = ('title','description','description_en','filmpas','slug','is_for','pk')

        widgets ={
            'slug':forms.HiddenInput(attrs={'readonly':'readonly','hidden':'hidden','value':'title'}),
            'is_for':forms.HiddenInput(attrs={'readonly':'readonly','hidden':'hidden','value':'serial'}),
        }
        labels = {
            'title':_('*review title'),'description':_('*review description'),'description_en':_('*review description en'),
            'filmpas':_('review preview'),'slug':'','is_for':'',
        }
        error_messages = {
            'title':{'required':_('this is fields required'),'max_length':_("this is field maximum character is 200")},
            'description':{'required':_('this is fields required'),},
            'description en':{'required':_('this is fields required'),},
        }


class FormReviewEdit(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('name', 'name_en', 'title', 'description', 'description_en', 'filmpas', 'slug')
        widgets ={
            'slug':forms.HiddenInput(attrs={'readonly':'readonly','hidden':'hidden'}),
        }
        labels = {
            'title':_('*review title'),'description':_('*review description'),'description_en':_('*review description en'),
            'filmpas':_('review preview'),'name':_('*review name'),'name en':_('*review name en'),'slug':'',
        }
        error_messages = {
            'title':{'required':_('this is fields required'),'max_length':_("this is field maximum character is 200")},
            'description':{'required':_('this is fields required'),},
            'description en':{'required':_('this is fields required'),},
        }
class FormContactForm(forms.Form):
    name = forms.CharField(
        label=_("Password sent"),
        error_messages=messages,
        required=True,
        widget=forms.TextInput(attrs={'placeholder':_("your name ..."), 'class':'name', 'type':'text'})
    )
    email = forms.CharField(
        label=_('your email'),
        error_messages=messages,
        required=True,
        widget= forms.TextInput(attrs = {'class':'email', 'placeholder':_('email ...'), 'type':'email'})
    )
    website = forms.CharField(
        label=_('your website'),
        error_messages=messages,
        required=False,
        widget=forms.TextInput(attrs={'class':'website', 'placeholder':_('website ...'), 'type':'text'})

    )
    message = forms.CharField(
        label=_('your message'),
        error_messages=messages,
        required=True,
        widget=forms.Textarea(attrs={'class':'message', 'placeholder':_('messsasge ...'),'type':'text'})
    )

