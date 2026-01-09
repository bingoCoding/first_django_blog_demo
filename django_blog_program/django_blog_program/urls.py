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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps import views as sitemap_views
from django.urls import path, re_path, include
from django.views.decorators.cache import cache_page
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter

from blog.apis import post_list_rest, PostListRest, PostViewSet, CategoryViewSet
from blog.rss import LatestPostFeed
from blog.sitemap import PostSiteMap
from blog.views import post_list, post_detail, PostDetailView, IndexView, CategoryView, TagView, SearchView
from comment.views import CommentView
from config.views import LinkListView
from django_blog_program.autocomplete import CategoryAutoComplete, TagAutoComplete
from django_blog_program.custom_site import custom_site


router = DefaultRouter()
router.register('post', PostViewSet, basename="api-post")
router.register('category', CategoryViewSet, basename="api-category")

urlpatterns = [
    path('admin/', custom_site.urls),
    path('super-admin/', admin.site.urls),

    #path("", post_list, name="post_list"),
    #re_path('category/(?P<category_id>\d+)/$', post_list, name="post_list"),
    #re_path('tag/(?P<tag_id>\d+)/$', post_list, name="post_list"),
    # re_path('post/(?P<post_id>\d+)/$', post_detail, name="post_detail"),
    # re_path('links/$', links, name="post_detail"),


    path("", IndexView.as_view(), name="post_list"),
    re_path('^/category/(?P<category_id>\d+)/$', CategoryView.as_view(), name="post_list"),
    re_path('^/tag/(?P<tag_id>\d+)/$', TagView.as_view(), name="post_list"),
    re_path('^/post/(?P<post_id>\d+)/', PostDetailView.as_view(), name="post_detail"),
    re_path('^/search/', SearchView.as_view(), name="post_list"),
    re_path('^/links/', LinkListView.as_view(), name="links"),
    re_path('^/comment/', CommentView.as_view(), name="comments"),
    re_path('^/rss|feed/', LatestPostFeed(), name="rss"),
    re_path('^/sitemap\.xml/$', cache_page(60*15, key_prefix='sitemap_cache_'), (sitemap_views.sitemap), {'sitemaps': {'posts': PostSiteMap}}, name="sitemap"),
    re_path('^/category-autocomplete/$', CategoryAutoComplete.as_view(), name="category-autocomplete"),
    re_path('^/tag-autocomplete/$', TagAutoComplete.as_view(), name="tag-autocomplete"),
    path('ckeditor/', include('ckeditor_uploader.urls')),

    # path('api/post/', post_list_rest, name="post_list_rest"),
    # path('api/post/', PostListRest.as_view(), name="post_list_rest"),

    path('api/', include(router.urls)),
    re_path('^api/docs/', include_docs_urls(title="Django Blog Program API"))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
