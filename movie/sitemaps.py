from django.contrib import sitemaps
from .models import Movie, Serial
from django.contrib.sitemaps import Sitemap


class MovieSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.9

    def items(self):
        return Movie.objects.all()

    def lastmod(self, obj):
        return obj.date


class SerialSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return Serial.objects.all()

    def lastmod(self, obj):
        return obj.date