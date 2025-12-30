from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.urls import reverse
from django.utils.html import format_html

from .admin_form import PostAdminForm
from .models import Category, Tag, Post
from django_blog_program.base_admin import BaseOwnerAdmin
from django_blog_program.custom_site import custom_site


# Register your models here.

class CategoryOwnerFilter(admin.SimpleListFilter):
    title = '分类过滤器'
    parameter_name = 'category_id'

    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list('id', 'name')

    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=category_id)
        return queryset

@admin.register(Post)
@admin.register(Post, site=custom_site)
class PostAdmin(BaseOwnerAdmin):
    form = PostAdminForm
    list_display = ('title', 'category', 'status', 'created_time', 'operator')
    list_display_links = ['title', 'category']

    list_filter = ('category', 'status', CategoryOwnerFilter)
    search_fields = ['title', 'category__name', 'tag__name']

    filter_horizontal = ('tag',)

    # fields = (('title', 'category'), 'desc', 'status', 'content', 'tag')
    fieldsets = (
        (
            '基础配置', {
                'description': '请填写文章标题、分类、标签和描述',
                'fields': ('title', 'category', 'status'),
                'classes': ['wide']
            }
        ),
        (
            '内容', {
                'fields': ('desc', 'content'),
            }
        ),
        (
            '额外信息', {
                'classes': ['collapse'],
                'fields': ('tag',),
            }
        )
    )

    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('admin:blog_post_change', args = (obj.id,))
        )
    operator.short_description = '操作'

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(PostAdmin, self).save_model(request, obj, form, change)

    def get_queryset(self, request):
        return super(PostAdmin, self).get_queryset(request).filter(owner=request.user)

    # class Media:
    #     css = {
    #         'all': ('custom_admin.css',)
    #     }
    #     js = ('custom_admin.js',)

class PostInLine(admin.StackedInline):
    model = Post
    fields = ('title', 'desc')
    extra = 1

@admin.register(Category)
class CategoryAdmin(BaseOwnerAdmin):
    inlines = [PostInLine]
    list_display = ('name', 'status', 'is_nav', 'created_time', 'owner')
    fields = ('name', 'status', 'is_nav')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(CategoryAdmin, self).save_model(request, obj, form, change)

    def post_count(self, obj):
        return obj.post_set.count()
    post_count.short_description = '文章数量'

@admin.register(Tag)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'created_time')
    fields = ('name', 'status')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(TagAdmin, self).save_model(request, obj, form, change)

@admin.register(LogEntry)
@admin.register(LogEntry, site=custom_site)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('object_repr', 'object_id', 'action_flag', 'user', 'change_message')