from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from pointless_impressions_src.artwork.models import Artwork


class ArtworkSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9
    protocol = 'https'

    def items(self):
        return Artwork.objects.filter(is_available=True)

    def lastmod(self, obj):
        return obj.updated_at


class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = "monthly"
    protocol = 'https'

    def items(self):
        return [
            'home',
            'artwork:list'
            ]

    def location(self, item):
        return reverse(item)
