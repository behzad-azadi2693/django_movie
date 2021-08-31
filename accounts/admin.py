from .models import User
from django.contrib import admin
from .forms import UserChangeForm, UserCreationForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


@admin.register(User)
class AdminUser(BaseUserAdmin):
    date_hierarchy = 'date_paid'
    
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('mobile','is_admin', 'is_active','otp', 'otp_create_time')
    list_filter = ('is_admin', )
    fieldsets = ( #this is for form
        (_('Information'),{'fields':('phone_number','date_paid','password')}),
        (_('personal info'),{'fields':('is_active','is_admin')}),
        (_('otp information'),{'fields':('otp',)}),
        (_('permission'),{'fields':('groups', 'user_permissions')}),
    )
    add_fieldsets = (#this is for add_form 
        (_('Information'),{'fields':('phone_number', 'password','password_confierm')}),
        (_('otp information'),{'fields':('otp',)}),
        (_('Access'),{'fields':('is_active','is_admin', 'groups', 'user_permissions')})
    )
    search_fields = ('phone_number',)
    ordering = ('phone_number',)
    filter_horizontal = ()

    actions = ('make_admin',)

    def make_admin(self, request, queryset):
        queryset.update(is_admin=True)

    def mobile(self,obj):
        return f'{obj.phone_number[:-7]}-{obj.phone_number[-7:-4]}-{obj.phone_number[-4:]}'

