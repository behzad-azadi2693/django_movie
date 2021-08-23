
from django import forms
from .models import User
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import ReadOnlyPasswordHashField



messages = {
    'required':_("this field is required"),
    'invalid':_("It is not correct"),
    'max_length':_("The size of the characters is large of 15 character"),
    'min_length':_("The size of the characters is small of 9 character"),
    'max_value':_("out of range maximum size"),
    'min_value':_("out of range minimum size"),
}

class UserCreationForm(forms.ModelForm):
    password = forms.CharField(label=_('password'), widget=forms.PasswordInput)
    password_confierm = forms.CharField(label=_('password_confierm'), widget=forms.PasswordInput)

    class Meta:
        models = User
        fields = ('phone_number', 'date_paid', 'password', 'password_confierm', 'otp', 'otp_create_time')

    def clean_password_confierm(self):
        cd = self.cleaned_data
        if cd['password'] and cd['password_confierm'] and cd['password'] != cd['password_confierm']:
            raise forms.ValidationError(_("password and confirm password must be match "))

        return cd['password_confierm']

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
        fields = ('phone_number', 'date_paid', 'password','otp', 'otp_create_time')

    def clean_password(self):
        return self.initial['password']
    

class UserPhoneForm(forms.Form):
    phone_number = forms.CharField(
        label=_("Password sent"),
        error_messages=messages,
        required=True,
        help_text=_("enter your phone number 09210000000..."),        
        widget=forms.TextInput(attrs={'placeholder':_("phone number ..."), 'class':'name', 'type':'number', 'value':None})
    )

    def clean_phone_number(self):
        cd = self.cleaned_data
        if cd['phone_number'] is None or cd['phone_number'] == '':
            raise forms.ValidationError(_('please check phone number'))
        return cd['phone_number']

class PasswordSms(forms.Form):
    password = forms.CharField(
        label=_("Password sent"),
        error_messages=messages,
        required=True,
        help_text=_("please neter password sent to you ... "),        
        widget=forms.TextInput(attrs={'placeholder':_("password sent ..."), 'class':'email', 'type':'number', 'value':None})
    )

    def clean_password(self):
        cd = self.cleaned_data
        if cd['password'] is None or cd['password'] == '':
            raise forms.ValidationError(_('please check sms number'))
        return cd['password']

