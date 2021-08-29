# Generated by Django 3.2.4 on 2021-08-24 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ContactUs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='your name')),
                ('email', models.EmailField(max_length=254, verbose_name='your email')),
                ('website', models.CharField(blank=True, max_length=100, null=True, verbose_name='your website')),
                ('message', models.TextField(verbose_name='your messaage')),
            ],
            options={
                'verbose_name': 'message table',
                'verbose_name_plural': 'messages table',
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='MessagesSending',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=300, verbose_name='subject email')),
                ('date', models.DateTimeField(verbose_name='date sendig email')),
                ('messages', models.TextField(verbose_name='message in email')),
            ],
            options={
                'verbose_name': 'messages sending',
                'verbose_name_plural': 'messages sendings',
            },
        ),
        migrations.CreateModel(
            name='NewsLetters',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=300, verbose_name='email user')),
            ],
            options={
                'verbose_name': 'news letter',
                'verbose_name_plural': 'news letters',
            },
        ),
    ]
