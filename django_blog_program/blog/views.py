from datetime import date

from django.core.cache import cache
from django.db.models import Q, F
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, ListView
from unicodedata import category

from comment.forms import CommentForm
from comment.models import Comment
from .models import Post, Category, Tag
from config.models import SideBar


# Create your views here.


class CommonViewMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'sidebars': SideBar.get_all(),
        })
        context.update(Category.get_navs())
        return context

class IndexView(CommonViewMixin, ListView):
    queryset = Post.latest_posts()
    paginate_by = 5
    context_object_name = 'post_list'
    template_name = 'blog/blog_list_view.html'

class PostListView(ListView):
    queryset = Post.latest_posts()
    paginate_by = 1
    context_object_name = 'post_list' #  默认为object_list
    template_name = 'blog/blog_list_view.html'

class PostDetailView(CommonViewMixin, DetailView):
    model = Post
    template_name = 'blog/blog_detail_view.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        # Post.objects.filter(pk=self.object.id).update(pv=F('pv') + 1, uv=F('uv') + 1)
        self.handler_visitor()

        # 调试
        from django.db import connection
        print(connection.queries)
        return response

    def handler_visitor(self):
        increate_pv = False
        increate_uv = False
        uid = self.request.uid
        pv_key = 'pv:%s:%s' % (uid, self.request.path)
        uv_key = 'uv:%s:%s:%s' % (uid, str(date.today()), self.request.path)
        if not cache.get(pv_key):
            increate_pv = True
            cache.set(pv_key, 1, 1 * 60) # 1 * 60 秒

        if not cache.get(uv_key):
            increate_uv = True
            cache.set(uv_key, 1, 24 * 60 * 60)

        if increate_pv or increate_uv:
            Post.objects.filter(pk=self.object.id).update(pv=F('pv') + 1, uv=F('uv') + 1)
        elif increate_uv:
            Post.objects.filter(pk=self.object.id).update(uv=F('uv') + 1)
        elif increate_pv:
            Post.objects.filter(pk=self.object.id).update(pv=F('pv') + 1)


    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context.update({
    #         'comment_form': CommentForm,
    #         'comment_list': Comment.get_by_target(self.request.path),
    #     })
    #     return context


class CategoryView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(Category, pk=category_id)
        context.update({
            'category': category,
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id)

class TagView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_id = self.kwargs.get('tag_id')
        tag = get_object_or_404(Tag, pk=tag_id)
        context.update({
            'tag': tag,
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        tag_id = self.kwargs.get('tag_id')
        return queryset.filter(tag__id=tag_id)

class SearchView(IndexView):
    def get_context_data(self):
        context = super().get_context_data()
        context.update({
            'keyword': self.request.GET.get('keyword', '')
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        keyword = self.request.GET.get('keyword')
        if not keyword:
            return queryset
        return queryset.filter(Q(title__icontains=keyword) | Q(desc__icontains=keyword))

def post_list(self, category_id=None, tag_id=None):
    tag = None
    category = None
    if tag_id:
        post_list, tag = Post.get_by_tag(tag_id = tag_id)
    elif category_id:
        post_list, category = Post.get_by_category(category_id=category_id)
    else:
        post_list = Post.latest_posts()
    context = {
        'post_list': post_list,
        'tag': tag,
        'category': category,
        'sidebars': SideBar.get_all(),
    }
    context.update(Category.get_navs())
    return render(self, 'blog/blog_list.html', context = context)

def post_detail(self, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        post = None
    context = {
        'post': post,
        'sidebars': SideBar.get_all(),
    }
    context.update(Category.get_navs())
    return render(self, 'blog/blog_detail.html', context = context)