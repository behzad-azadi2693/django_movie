from django.contrib import messages
from django.db import models
from django.urls import reverse
from config.settings import USE_I18N
from datetime import date, datetime, timedelta
from django.contrib.sessions.models import Session
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
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
    otp_create_time = models.DateTimeField(null=True, blank=True)

    save = GenericRelation('Save')
    

    is_active = models.BooleanField(default=True, verbose_name=_("user is active"))
    is_admin = models.BooleanField(default=False, verbose_name=_("user is admin"))
    
    objects=MyUserManager()
    USERNAME_FIELD = 'phone_number'

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

class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name=_("category name"))
    name_en = models.CharField(max_length=200, verbose_name=_("category name en"))

    def __str__(self) -> str:
        return f'{self.name}-{self.name_en}'


class Movie(models.Model):
    MOVIE_CHOICE = (
    ("iranian", "iranian"),
    ("halliwood", "halliwood"),
    ("balliwood", "balliwood"),
    ("arabic", "arabic"),
    ("chaina", "chaina"),
    ("turkish", "turkish"),
    ("child","child"),
    ("animate","animate")
    )
    name = models.CharField(max_length=200, verbose_name=_("movie name"))    
    name_en = models.CharField(max_length=200, verbose_name=_("movie name en"))
    title = models.CharField(max_length=200, verbose_name=_("movie title"))
    slug = models.SlugField(allow_unicode=True, verbose_name=_("movie slug"))
    gener = models.CharField(max_length=250, verbose_name=_("movie gener"))
    gener_en = models.CharField(max_length=250, verbose_name=_("movie gener en"))
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, related_name='category_film', verbose_name=_("film category"))
    description = models.TextField(verbose_name=_("movie description"))
    description_en = models.TextField(verbose_name=_("movie description en"))
    date = models.DateField(verbose_name=_("movie date create"))
    ratin = models.PositiveIntegerField(null=True, blank=True,verbose_name=_("movie ratin of 10"))
    awards = models.CharField(max_length=500, null=True, blank=True, verbose_name=_("movie awards"))
    image = models.ImageField(upload_to='film/awatar/',verbose_name=_("movie awatar"))
    filmpas = models.FileField(upload_to='film/pass/',verbose_name=_("movie preview"))
    film1080 = models.FileField(upload_to = 'film/1080/', null=True, blank=True, verbose_name=_("movie quality 1080"))
    filme720 = models.FileField(upload_to='film/720/', null=True, blank=True, verbose_name=_("movie quality 720"))
    film480 = models.FileField(upload_to='film480/', null=True, blank=True, verbose_name=_("movie quality 1080"))
    subtitle = models.FileField(upload_to='trans/', null=True, blank=True, verbose_name=_("movie subtitle"))
    category = models.ForeignKey(Category,related_name='cat_movie', on_delete=models.DO_NOTHING, null=True, blank=True)
    director = models.CharField(max_length=250, null=True, blank=True, default=_("None"), verbose_name=_("movie director"))
    writer = models.CharField(max_length=250,  null=True, blank=True,default=_("None"), verbose_name=_("movie writer"))
    stars = models.CharField(max_length=400, null=True, blank=True, default=_("None"), verbose_name=_("movie stars"))
    time = models.TimeField(null=True, blank=True,verbose_name=_("movie time"))
    is_a = models.CharField(default='movie', max_length=5)
    choice = models.CharField(choices=MOVIE_CHOICE, max_length=15, verbose_name=_("movie choice"))
    review_movie = GenericRelation('Review')
    save_movie = GenericRelation('Save')

    class Meta:
        verbose_name = _("movie table")
        verbose_name_plural = _("movies table")
        ordering = ('-id',)

    def get_absolute_url(self):
        return reverse('movie:film', args=(self.slug,))
    
    def save(self, *args, **kwargs):
            slti = self.title.replace(' ','-') 
            self.slug = slti
            super(Movie, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.slug




class ContactUs(models.Model):
    name = models.CharField(max_length=250, verbose_name= _("your name"))
    email = models.EmailField(verbose_name=_("your email"))
    website = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("your website"))
    message = models.TextField(verbose_name= _("your messaage"))

    class Meta:
        verbose_name = _("message table")
        verbose_name_plural = _("messages table")
        ordering = ('-id',)


    def __str__(self) -> str:
        return f'{self.name}-{self.email}'


class Serial(models.Model):
    SERIAL_CHOICE = (
    ("iranian", "iranian"),
    ("halliwood", "halliwood"),
    ("balliwood", "balliwood"),
    ("arabic", "arabic"),
    ("chaina", "chaina"),
    ("turkish", "turkish"),
    ("child","child"),
    ("animate","animate")
    )
    name = models.CharField(max_length=200, verbose_name= _("serial name"))
    name_en = models.CharField(max_length=200, verbose_name=_("serial name en"))
    title = models.CharField(max_length=200, verbose_name=_("serial title"))
    slug = models.SlugField(allow_unicode=True, verbose_name=_("serial slug"))
    description = models.TextField(verbose_name=_("serial description"))
    description_en = models.TextField(verbose_name=_("serial description en"))
    image = models.ImageField(upload_to='serial/awatar/', verbose_name=_("serial awatar"))
    date = models.DateField(verbose_name=_("serial create date"))
    awards = models.CharField(max_length=500, null=True, blank=True, verbose_name=_("movie awards"))
    ratin = models.PositiveIntegerField(verbose_name=_("serial ratin of 10"), null=True, blank=True,)
    filmpas = models.FileField(upload_to='serial/pass/',verbose_name=_("serial preview"))
    gener = models.CharField(max_length=250, verbose_name= _("serial gener"))
    gener_en = models.CharField(max_length=250, verbose_name=_("serial gener en"))
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, related_name='category_serial', verbose_name=_("serial category"))
    director = models.CharField(max_length=250, default=_("None"), verbose_name= _("serial director"), null=True, blank=True)
    writer = models.CharField(max_length=250, default=_("None"), verbose_name=_("serial writer"), null=True, blank=True)
    stars = models.CharField(max_length=400, default=_("None"), verbose_name=_("serial stars"), null=True, blank=True)
    time = models.TimeField(verbose_name=_("serial time"), null=True, blank=True)
    is_a = models.CharField(default='serial', max_length=6)
    choice = models.CharField(choices=SERIAL_CHOICE, max_length=15, verbose_name=_("serial choices"))
    review_serial = GenericRelation('Review')
    save_serial = GenericRelation('Save')

    class Meta:
        verbose_name = _("serial table")
        verbose_name_plural = _("serials table")
        ordering = ('-id',)

    def get_absolute_url(self):
        return reverse('movie:serial', args=(self.slug,))
    
    def save(self, *args, **kwargs):
            slti = self.title.replace(' ','-')
            self.slug = slti
            super(Serial, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name



class SerialSession(models.Model):
    session = models.PositiveIntegerField(verbose_name=_('serial session'))
    title = models.CharField(max_length=200, verbose_name=_("serial session title"),help_text=_('session one of serial name'))
    slug = models.SlugField(allow_unicode=True, verbose_name=_("serial session slug"))
    serial = models.ForeignKey(Serial, related_name='sessions_serial',on_delete=models.CASCADE)
    subtitle = models.FileField(upload_to='serial/trans/', null=True, blank=True, verbose_name=_("serial subtitle"))
    ordering = ('-id',)

    class Meta:
        verbose_name = 'serial session table'
        verbose_name_plural = 'serials session table'

    def get_absulote_url(self):
        return reverse('movie:serial_session', args=(self.slug,))
    
    def save(self, *args, **kwargs):
        slti = self.title.replace(' ','-') 
        self.slug = slti            
        super(SerialSession, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.session}'

class SerialFilms(models.Model):
    episod = models.PositiveIntegerField(help_text='01', verbose_name=_("serial episod"))
    title = models.CharField(max_length=200, verbose_name=_("serial title"),help_text=_('episod one of session tow serial name'))
    slug = models.SlugField(allow_unicode=True, verbose_name=_("serial slug"))
    serial = models.ForeignKey(Serial, on_delete=models.CASCADE, related_name='serial_film', verbose_name=_("serial relation"))
    session = models.ForeignKey(SerialSession, related_name='serial_session', verbose_name=_('serial film session'), on_delete=models.CASCADE)
    serial1080 = models.FileField(upload_to='serial/1080/', null=True, blank=True, verbose_name=_("serial quality 1080"))
    serial720 = models.FileField(upload_to='serial/720', null=True, blank=True, verbose_name=_("serial quality 720"))
    serial480 = models.FileField(upload_to='serial/480', null=True, blank=True, verbose_name=_("serial quality 480"))

    class Meta:
        verbose_name = 'serial related table'
        verbose_name_plural = 'serials related table'
        ordering = ('-id',)

    def get_absulote_url(self):
        return reverse('movie:serial_single', args=(self.slug,))
    
    def save(self, *args, **kwargs):
        slti = self.title.replace(' ','-') 
        self.slug = slti
        super(SerialFilms, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.episod}'


class Review(models.Model):
    REVIEW_CHOICE = (
        ("serial", "serial"),
        ("movie", "movie"),
    )
    name = models.CharField(max_length=200, verbose_name=_('review name'))
    name_en = models.CharField(max_length=200, verbose_name=_("review name en"))
    title = models.CharField(max_length=200, verbose_name=_("serial title"))
    slug = models.SlugField(allow_unicode=True, verbose_name=_("serial slug"))
    description = models.TextField(verbose_name=_("serial description"))
    description_en = models.TextField(verbose_name=_("serial description en"))
    is_for = models.CharField(choices=REVIEW_CHOICE, max_length=15, verbose_name=_("is for"))
    filmpas = models.FileField(upload_to='review/film/', verbose_name=_( "preview"), null=True, blank=True)
    object_id = models.PositiveIntegerField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    content_object = GenericForeignKey('content_type', 'object_id')
    choice = models.CharField(max_length=30)

    class Meta:
        verbose_name = _("review table")
        verbose_name_plural = _("reviews table")    
        ordering = ('-id',)

    
    def get_absolute_url(self):
        return reverse('movie:singel_review', args=(self.slug,))

    def save(self, *args, **kwargs):
        slti = self.title.replace(' ','-') 
        self.slug = slti        
        super(Review, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title


class Save(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    content_object = GenericForeignKey('content_type', 'object_id')


    class Meta:
        verbose_name = _("save table")
        verbose_name_plural = _("saves table")    
        ordering = ('-id',)


class SessionUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions', verbose_name=_('user name'))
    session_key = models.ForeignKey(Session, on_delete=models.CASCADE, verbose_name=_('session key'))
    device = models.CharField(max_length=300, verbose_name=_('device name'))
    os = models.CharField(max_length=300, verbose_name=_('os name'))
    date_joiin = models.DateField(verbose_name=_('date join device'))
    ip_device = models.GenericIPAddressField(verbose_name=_('ip address device'))


    class Meta:
        verbose_name = _('session user device')        
        verbose_name_plural = _("ssessions user devices")
        ordering = ('-id',)


class HistoryPaid(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='history_paid', verbose_name=_('history paid'))
    date = models.DateTimeField(verbose_name=_('date paid'))
    price = models.PositiveIntegerField(verbose_name=_('amount of price'))
    code = models.CharField(max_length=150, verbose_name=_('payment code'))

    class Meta:
        verbose_name = _('history user paid')        
        verbose_name_plural = _("histories user paid")
        ordering = ('-id',)

    def __str__(self):
        return self.date 


class NewsLetters(models.Model):
    email = models.EmailField(max_length=300, verbose_name=_('email user'))

    class Meta:
        verbose_name = _('news letter')
        verbose_name_plural = _('news letters')

    def __str__(self):
        return self.email


class MessagesSending(models.Model):
    subject = models.CharField(max_length=300, verbose_name=_('subject email'))
    date = models.DateTimeField(verbose_name=_('date sendig email'))
    messages = models.TextField(verbose_name=_('message in email'))
    
    class Meta:
      verbose_name = _('messages sending')
      verbose_name_plural = _('messages sendings')
  
    def __str__(self):
      return self.subject