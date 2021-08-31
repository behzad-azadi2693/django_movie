from django.db import models
from datetime import datetime,timedelta
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.

class  MyUserManager(BaseUserManager):
    def create_user(self, phone_number, password):
        if not phone_number:
            raise ValueError(_("please insert phone number"))
        user = self.model(phone_number=phone_number)
        user.set_password(password)
        user.save(using=self._db)
        return user 

    def create_superuser(self, phone_number, password):
        user = self.create_user(phone_number=phone_number, password=password)
        user.is_admin=True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser,PermissionsMixin):
    date_paid = models.DateTimeField(null=True, blank=True, default=None)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message=_("Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."))
    phone_number = models.CharField(validators=[phone_regex], max_length=17, unique=True, verbose_name=_("your phone number") ) # validators should be a list
    otp = models.PositiveIntegerField(null=True, blank=True)
    otp_create_time = models.DateTimeField(auto_now=True, null=True, blank=True)

    save = GenericRelation('Save')
    

    is_active = models.BooleanField(default=True, verbose_name=_("user is active"))
    is_admin = models.BooleanField(default=False, verbose_name=_("user is admin"))
    
    objects=MyUserManager()
    USERNAME_FIELD = 'phone_number'
    
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        app_label = 'accounts'

    def __str__(self) -> str:
        return self.phone_number

    def is_paid(self):
        if self.date_paid:
            after_month = self.date_paid + timedelta(days=31)
            today = datetime.now()
            if after_month.date()>today.date():
                return True
            else:
                return False
        else:
            return False

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
        
    @property
    def is_staff(self):
        return self.is_admin

    def save(self, *args, **kwargs):
        """saving to DB disabled"""
        super(User, self).save(*args, **kwargs)
