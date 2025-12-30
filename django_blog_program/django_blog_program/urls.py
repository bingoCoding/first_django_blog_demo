"""
URL configuration for django_blog_program project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.sitemaps import views as sitemap_views
from django.urls import path, re_path

from blog.rss import LatestPostFeed
from blog.sitemap import PostSiteMap
from blog.views import post_list, post_detail, PostDetailView, IndexView, CategoryView, TagView, SearchView
from comment.views import CommentView
from config.views import LinkListView
from django_blog_program.custom_site import custom_site

urlpatterns = [
    path('admin/', custom_site.urls),
    path('super-admin/', admin.site.urls),

    #path("", post_list, name="post_list"),
    #re_path('category/(?P<category_id>\d+)/$', post_list, name="post_list"),
    #re_path('tag/(?P<tag_id>\d+)/$', post_list, name="post_list"),
    # re_path('post/(?P<post_id>\d+)/$', post_detail, name="post_detail"),
    # re_path('links/$', links, name="post_detail"),


    path("", IndexView.as_view(), name="post_list"),
    re_path('category/(?P<category_id>\d+)/$', CategoryView.as_view(), name="post_list"),
    re_path('tag/(?P<tag_id>\d+)/$', TagView.as_view(), name="post_list"),
    re_path('post/(?P<post_id>\d+)/', PostDetailView.as_view(), name="post_detail"),
    re_path('search/', SearchView.as_view(), name="post_list"),
    re_path('links/', LinkListView.as_view(), name="links"),
    re_path('comment/', CommentView.as_view(), name="comments"),
    re_path('^rss|feed/', LatestPostFeed(), name="rss"),
    re_path('^sitemap\.xml/$', sitemap_views.sitemap, {'sitemaps': {'posts': PostSiteMap}}, name="comments"),
]
