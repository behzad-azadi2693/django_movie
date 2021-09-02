from django.db import models
from django.urls import reverse
from accounts.models import User
from rest_framework.authtoken.models import Token
from django.contrib.sessions.models import Session
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation

# Create your models here

class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name=_("category name"))
    name_en = models.CharField(max_length=200, verbose_name=_("category name en"))

    def __str__(self) -> str:
        return f'{self.name}-{self.name_en}'

    class Meta:
        app_label = 'accounts'

def path_save_movie(instance, filename):
    name = '/'.join(filter(None, (instance.name_en, filename)))
    return 'movie/'+name

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
    title = models.CharField(max_length=200, verbose_name=_("movie title"), unique=True)
    slug = models.SlugField(allow_unicode=True, verbose_name=_("movie slug"))
    gener = models.CharField(max_length=250, verbose_name=_("movie gener"))
    gener_en = models.CharField(max_length=250, verbose_name=_("movie gener en"))
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, related_name='category_film', verbose_name=_("film category"))
    description = models.TextField(verbose_name=_("movie description"))
    description_en = models.TextField(verbose_name=_("movie description en"))
    date = models.DateField(verbose_name=_("movie date create"))
    ratin = models.PositiveIntegerField(null=True, blank=True,verbose_name=_("movie ratin of 10"))
    awards = models.CharField(max_length=500, null=True, blank=True, verbose_name=_("movie awards"))
    image = models.ImageField(upload_to=path_save_movie,verbose_name=_("movie awatar"))
    filmpas = models.FileField(upload_to=path_save_movie,verbose_name=_("movie preview"))
    film1080 = models.FileField(upload_to = path_save_movie, null=True, blank=True, verbose_name=_("movie quality 1080"))
    filme720 = models.FileField(upload_to=path_save_movie, null=True, blank=True, verbose_name=_("movie quality 720"))
    film480 = models.FileField(upload_to=path_save_movie, null=True, blank=True, verbose_name=_("movie quality 1080"))
    subtitle = models.FileField(upload_to=path_save_movie, null=True, blank=True, verbose_name=_("movie subtitle"))
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
        app_label = 'accounts'

    def get_absolute_url(self):
        return reverse('movie:film', args=(self.slug,))
    
    def save(self, *args, **kwargs):
            slti = self.title.replace(' ','-') 
            self.slug = slti
            super(Movie, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.slug


def path_save_serial(instance, filename):
    name = '{0}/{1}'.format(instance.name_en,  filename)
    return 'serial/'+name

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
    title = models.CharField(max_length=200, verbose_name=_("serial title"), unique=True)
    slug = models.SlugField(allow_unicode=True, verbose_name=_("serial slug"))
    description = models.TextField(verbose_name=_("serial description"))
    description_en = models.TextField(verbose_name=_("serial description en"))
    image = models.ImageField(upload_to=path_save_serial, verbose_name=_("serial awatar"))
    date = models.DateField(verbose_name=_("serial create date"))
    awards = models.CharField(max_length=500, null=True, blank=True, verbose_name=_("movie awards"))
    ratin = models.PositiveIntegerField(verbose_name=_("serial ratin of 10"), null=True, blank=True,)
    filmpas = models.FileField(upload_to=path_save_serial,verbose_name=_("serial preview"))
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
        app_label = 'accounts'

    def get_absolute_url(self):
        return reverse('movie:serial', args=(self.slug,))
    
    def save(self, *args, **kwargs):
            slti = self.title.replace(' ','-')
            self.slug = slti
            super(Serial, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


def path_save_session(instance, filename):
    name = '{0}/session{1}/{2}'.format(instance.serial.name_en, instance.session, filename)
    return 'serial/'+name

class SerialSession(models.Model):
    session = models.PositiveIntegerField(verbose_name=_('serial session'))
    title = models.CharField(max_length=200, unique=True,verbose_name=_("serial session title"),help_text=_('session one of serial name'))
    slug = models.SlugField(allow_unicode=True, verbose_name=_("serial session slug"))
    serial = models.ForeignKey(Serial, related_name='sessions_serial',on_delete=models.CASCADE)
    subtitle = models.FileField(upload_to=path_save_session, null=True, blank=True, verbose_name=_("serial subtitle"))

    class Meta:
        verbose_name = 'serial session table'
        verbose_name_plural = 'serials session table'
        app_label = 'accounts'
        ordering = ('-id',)

    def get_absulote_url(self):
        return reverse('movie:serial_session', args=(self.slug,))
    
    def save(self, *args, **kwargs):
        slti = self.title.replace(' ','-') 
        self.slug = slti            
        super(SerialSession, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.session}'
 

def path_save_key_session(instance, filename):
    name = '{0}/session{1}/{2}'.format(instance.serial.name_en, instance.session.session, filename)
    return 'serial/'+name

class SerialFilms(models.Model):
    episod = models.PositiveIntegerField(help_text='01', verbose_name=_("serial episod"))
    title = models.CharField(max_length=200, unique=True,verbose_name=_("serial title"),help_text=_('episod one of session tow serial name'))
    slug = models.SlugField(allow_unicode=True, verbose_name=_("serial slug"))
    serial = models.ForeignKey(Serial, on_delete=models.CASCADE, related_name='serial_film', verbose_name=_("serial relation"))
    session = models.ForeignKey(SerialSession, related_name='serial_session', verbose_name=_('serial film session'), on_delete=models.CASCADE)
    serial1080 = models.FileField(upload_to=path_save_key_session, null=True, blank=True, verbose_name=_("serial quality 1080"))
    serial720 = models.FileField(upload_to=path_save_key_session, null=True, blank=True, verbose_name=_("serial quality 720"))
    serial480 = models.FileField(upload_to=path_save_key_session, null=True, blank=True, verbose_name=_("serial quality 480"))

    class Meta:
        verbose_name = 'serial related table'
        verbose_name_plural = 'serials related table'
        ordering = ('-id',)
        app_label = 'accounts'

    def get_absulote_url(self):
        return reverse('movie:serial_single', args=(self.slug,))
    
    def save(self, *args, **kwargs):
        slti = self.title.replace(' ','-') 
        self.slug = slti
        super(SerialFilms, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.episod}'


def path_save_review(instance, filename):
    name = '/'.join(filter(None, (instance.name_en, filename)))
    return 'review/'+name

class Review(models.Model):
    REVIEW_CHOICE = (
        ("serial", "serial"),
        ("movie", "movie"),
    )
    name = models.CharField(max_length=200, verbose_name=_('review name'))
    name_en = models.CharField(max_length=200, verbose_name=_("review name en"))
    title = models.CharField(max_length=200, verbose_name=_("serial title"), unique=True)
    slug = models.SlugField(allow_unicode=True, verbose_name=_("serial slug"))
    description = models.TextField(verbose_name=_("serial description"))
    description_en = models.TextField(verbose_name=_("serial description en"))
    is_for = models.CharField(choices=REVIEW_CHOICE, max_length=15, verbose_name=_("is for"))
    filmpas = models.FileField(upload_to= path_save_review, verbose_name=_( "preview"), null=True, blank=True)
    object_id = models.PositiveIntegerField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    content_object = GenericForeignKey('content_type', 'object_id')
    choice = models.CharField(max_length=30)

    class Meta:
        verbose_name = _("review table")
        verbose_name_plural = _("reviews table")    
        ordering = ('-id',)
        app_label = 'accounts'

    
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
        app_label = 'accounts'


class SessionUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions', verbose_name=_('user name'))
    session_key = models.ForeignKey(Session, on_delete=models.CASCADE, verbose_name=_('session key'))
    device = models.CharField(max_length=300, verbose_name=_('device name'))
    os = models.CharField(max_length=300, verbose_name=_('os name'))
    date_joiin = models.DateField(verbose_name=_('date join device'))
    ip_device = models.GenericIPAddressField(verbose_name=_('ip address device'))
    token = models.ForeignKey(Token, on_delete=models.CASCADE, verbose_name=_('Token user'))


    class Meta:
        verbose_name = _('session user device')        
        verbose_name_plural = _("ssessions user devices")
        ordering = ('-id',)
        app_label = 'accounts'


class HistoryPaid(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='history_paid', verbose_name=_('history paid'))
    date = models.DateTimeField(verbose_name=_('date paid'))
    price = models.PositiveIntegerField(verbose_name=_('amount of price'))
    code = models.CharField(max_length=150, verbose_name=_('payment code'))

    class Meta:
        verbose_name = _('history user paid')        
        verbose_name_plural = _("histories user paid")
        ordering = ('-id',)
        app_label = 'accounts'

    def __str__(self):
        return self.date 


class NewsLetters(models.Model):
    email = models.EmailField(max_length=300, verbose_name=_('email user'))

    class Meta:
        verbose_name = _('news letter')
        verbose_name_plural = _('news letters')
        app_label = 'movie'

    def __str__(self):
        return self.email


class MessagesSending(models.Model):
    subject = models.CharField(max_length=300, verbose_name=_('subject email'))
    date = models.DateTimeField(verbose_name=_('date sendig email'), auto_now_add=True)
    messages = models.TextField(verbose_name=_('message in email'))
    
    class Meta:
        verbose_name = _('messages sending')
        verbose_name_plural = _('messages sendings')
        app_label = 'movie'

    def __str__(self):
      return self.subject




class ContactUs(models.Model):
    name = models.CharField(max_length=250, verbose_name= _("your name"))
    email = models.EmailField(verbose_name=_("your email"))
    website = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("your website"))
    message = models.TextField(verbose_name= _("your messaage"))

    class Meta:
        verbose_name = _("message table")
        verbose_name_plural = _("messages table")
        ordering = ('-id',)
        app_label = 'movie'

    def __str__(self) -> str:
        return f'{self.name}-{self.email}'
