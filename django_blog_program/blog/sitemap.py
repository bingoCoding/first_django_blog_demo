from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from blog.models import Post


class PostSiteMap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9
    protocol = 'https'

    def items(self):
        return Post.objects.filter(status=Post.STATUS_NORMAL)

    def lastmod(self, obj):
        return obj.created_time

    def location(self, obj):
        return reverse('post_detail', args = [obj.id])