# Generated by Django 3.2.4 on 2021-09-02 11:52

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import movie.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sessions', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('date_paid', models.DateTimeField(blank=True, default=None, null=True)),
                ('phone_number', models.CharField(max_length=17, unique=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')], verbose_name='your phone number')),
                ('otp', models.PositiveIntegerField(blank=True, null=True)),
                ('otp_create_time', models.DateTimeField(auto_now=True, null=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='user is active')),
                ('is_admin', models.BooleanField(default=False, verbose_name='user is admin')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='category name')),
                ('name_en', models.CharField(max_length=200, verbose_name='category name en')),
            ],
        ),
        migrations.CreateModel(
            name='Serial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='serial name')),
                ('name_en', models.CharField(max_length=200, verbose_name='serial name en')),
                ('title', models.CharField(max_length=200, unique=True, verbose_name='serial title')),
                ('slug', models.SlugField(allow_unicode=True, verbose_name='serial slug')),
                ('description', models.TextField(verbose_name='serial description')),
                ('description_en', models.TextField(verbose_name='serial description en')),
                ('image', models.ImageField(upload_to=movie.models.path_save_serial, verbose_name='serial awatar')),
                ('date', models.DateField(verbose_name='serial create date')),
                ('awards', models.CharField(blank=True, max_length=500, null=True, verbose_name='movie awards')),
                ('ratin', models.PositiveIntegerField(blank=True, null=True, verbose_name='serial ratin of 10')),
                ('filmpas', models.FileField(upload_to=movie.models.path_save_serial, verbose_name='serial preview')),
                ('gener', models.CharField(max_length=250, verbose_name='serial gener')),
                ('gener_en', models.CharField(max_length=250, verbose_name='serial gener en')),
                ('director', models.CharField(blank=True, default='None', max_length=250, null=True, verbose_name='serial director')),
                ('writer', models.CharField(blank=True, default='None', max_length=250, null=True, verbose_name='serial writer')),
                ('stars', models.CharField(blank=True, default='None', max_length=400, null=True, verbose_name='serial stars')),
                ('time', models.TimeField(blank=True, null=True, verbose_name='serial time')),
                ('is_a', models.CharField(default='serial', max_length=6)),
                ('choice', models.CharField(choices=[('iranian', 'iranian'), ('halliwood', 'halliwood'), ('balliwood', 'balliwood'), ('arabic', 'arabic'), ('chaina', 'chaina'), ('turkish', 'turkish'), ('child', 'child'), ('animate', 'animate')], max_length=15, verbose_name='serial choices')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='category_serial', to='accounts.category', verbose_name='serial category')),
            ],
            options={
                'verbose_name': 'serial table',
                'verbose_name_plural': 'serials table',
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='SessionUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device', models.CharField(max_length=300, verbose_name='device name')),
                ('os', models.CharField(max_length=300, verbose_name='os name')),
                ('date_joiin', models.DateField(verbose_name='date join device')),
                ('ip_device', models.GenericIPAddressField(verbose_name='ip address device')),
                ('session_key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sessions.session', verbose_name='session key')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sessions', to=settings.AUTH_USER_MODEL, verbose_name='user name')),
            ],
            options={
                'verbose_name': 'session user device',
                'verbose_name_plural': 'ssessions user devices',
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='SerialSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session', models.PositiveIntegerField(verbose_name='serial session')),
                ('title', models.CharField(help_text='session one of serial name', max_length=200, unique=True, verbose_name='serial session title')),
                ('slug', models.SlugField(allow_unicode=True, verbose_name='serial session slug')),
                ('subtitle', models.FileField(blank=True, null=True, upload_to=movie.models.path_save_session, verbose_name='serial subtitle')),
                ('serial', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sessions_serial', to='accounts.serial')),
            ],
            options={
                'verbose_name': 'serial session table',
                'verbose_name_plural': 'serials session table',
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='SerialFilms',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('episod', models.PositiveIntegerField(help_text='01', verbose_name='serial episod')),
                ('title', models.CharField(help_text='episod one of session tow serial name', max_length=200, unique=True, verbose_name='serial title')),
                ('slug', models.SlugField(allow_unicode=True, verbose_name='serial slug')),
                ('serial1080', models.FileField(blank=True, null=True, upload_to=movie.models.path_save_key_session, verbose_name='serial quality 1080')),
                ('serial720', models.FileField(blank=True, null=True, upload_to=movie.models.path_save_key_session, verbose_name='serial quality 720')),
                ('serial480', models.FileField(blank=True, null=True, upload_to=movie.models.path_save_key_session, verbose_name='serial quality 480')),
                ('serial', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='serial_film', to='accounts.serial', verbose_name='serial relation')),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='serial_session', to='accounts.serialsession', verbose_name='serial film session')),
            ],
            options={
                'verbose_name': 'serial related table',
                'verbose_name_plural': 'serials related table',
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='Save',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'save table',
                'verbose_name_plural': 'saves table',
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='review name')),
                ('name_en', models.CharField(max_length=200, verbose_name='review name en')),
                ('title', models.CharField(max_length=200, unique=True, verbose_name='serial title')),
                ('slug', models.SlugField(allow_unicode=True, verbose_name='serial slug')),
                ('description', models.TextField(verbose_name='serial description')),
                ('description_en', models.TextField(verbose_name='serial description en')),
                ('is_for', models.CharField(choices=[('serial', 'serial'), ('movie', 'movie')], max_length=15, verbose_name='is for')),
                ('filmpas', models.FileField(blank=True, null=True, upload_to=movie.models.path_save_review, verbose_name='preview')),
                ('object_id', models.PositiveIntegerField()),
                ('choice', models.CharField(max_length=30)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
            options={
                'verbose_name': 'review table',
                'verbose_name_plural': 'reviews table',
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='movie name')),
                ('name_en', models.CharField(max_length=200, verbose_name='movie name en')),
                ('title', models.CharField(max_length=200, unique=True, verbose_name='movie title')),
                ('slug', models.SlugField(allow_unicode=True, verbose_name='movie slug')),
                ('gener', models.CharField(max_length=250, verbose_name='movie gener')),
                ('gener_en', models.CharField(max_length=250, verbose_name='movie gener en')),
                ('description', models.TextField(verbose_name='movie description')),
                ('description_en', models.TextField(verbose_name='movie description en')),
                ('date', models.DateField(verbose_name='movie date create')),
                ('ratin', models.PositiveIntegerField(blank=True, null=True, verbose_name='movie ratin of 10')),
                ('awards', models.CharField(blank=True, max_length=500, null=True, verbose_name='movie awards')),
                ('image', models.ImageField(upload_to=movie.models.path_save_movie, verbose_name='movie awatar')),
                ('filmpas', models.FileField(upload_to=movie.models.path_save_movie, verbose_name='movie preview')),
                ('film1080', models.FileField(blank=True, null=True, upload_to=movie.models.path_save_movie, verbose_name='movie quality 1080')),
                ('filme720', models.FileField(blank=True, null=True, upload_to=movie.models.path_save_movie, verbose_name='movie quality 720')),
                ('film480', models.FileField(blank=True, null=True, upload_to=movie.models.path_save_movie, verbose_name='movie quality 1080')),
                ('subtitle', models.FileField(blank=True, null=True, upload_to=movie.models.path_save_movie, verbose_name='movie subtitle')),
                ('director', models.CharField(blank=True, default='None', max_length=250, null=True, verbose_name='movie director')),
                ('writer', models.CharField(blank=True, default='None', max_length=250, null=True, verbose_name='movie writer')),
                ('stars', models.CharField(blank=True, default='None', max_length=400, null=True, verbose_name='movie stars')),
                ('time', models.TimeField(blank=True, null=True, verbose_name='movie time')),
                ('is_a', models.CharField(default='movie', max_length=5)),
                ('choice', models.CharField(choices=[('iranian', 'iranian'), ('halliwood', 'halliwood'), ('balliwood', 'balliwood'), ('arabic', 'arabic'), ('chaina', 'chaina'), ('turkish', 'turkish'), ('child', 'child'), ('animate', 'animate')], max_length=15, verbose_name='movie choice')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='category_film', to='accounts.category', verbose_name='film category')),
            ],
            options={
                'verbose_name': 'movie table',
                'verbose_name_plural': 'movies table',
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='HistoryPaid',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(verbose_name='date paid')),
                ('price', models.PositiveIntegerField(verbose_name='amount of price')),
                ('code', models.CharField(max_length=150, verbose_name='payment code')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='history_paid', to=settings.AUTH_USER_MODEL, verbose_name='history paid')),
            ],
            options={
                'verbose_name': 'history user paid',
                'verbose_name_plural': 'histories user paid',
                'ordering': ('-id',),
            },
        ),
    ]
