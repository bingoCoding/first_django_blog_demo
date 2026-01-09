from django.http import JsonResponse
from django.template.context_processors import request
from rest_framework import generics, viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from unicodedata import category

from blog.models import Post, Category
from blog.serializers import PostSerializer, PostDetailSerializer, CategorySerializer, CategoryDetailSerializer


class PostViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.filter(status=Post.STATUS_NORMAL)
    # permission_classes =  [IsAdminUser] # 写入时的权限

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = PostDetailSerializer
        return super().retrieve(request, *args, **kwargs)

    def filter_queryset(self, queryset):
        category_id = self.request.query_params.get('category_id')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.filter(status=Category.STATUS_NORMAL)

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = CategoryDetailSerializer
        return super().retrieve(request, *args, **kwargs)

class PostListRest(generics.ListCreateAPIView):
    queryset = Post.objects.filter(status=Post.STATUS_NORMAL)
    serializer_class = PostSerializer


@api_view(['GET', 'POST'])
def post_list_rest(request):
    posts = Post.objects.filter(status=Post.STATUS_NORMAL)
    posts_serializer = PostSerializer(posts, many=True)
    return Response(posts_serializer.data)

