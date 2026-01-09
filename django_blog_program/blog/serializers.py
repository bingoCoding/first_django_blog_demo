from rest_framework import serializers, pagination

from blog.models import Post, Category


class PostSerializer(serializers.HyperlinkedModelSerializer):  # serializers.ModelSerializer
    url = serializers.HyperlinkedIdentityField(view_name='api-post-detail')

    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    tag = serializers.SlugRelatedField(slug_field='name', many=True, read_only=True)
    owner = serializers.SlugRelatedField(slug_field='username', read_only=True)
    created_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Post
        fields = ('url', 'id', 'title', 'category', 'tag', 'owner', 'created_time')

class PostDetailSerializer(PostSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'category', 'tag', 'owner', 'content_html', 'created_time')

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'is_nav', 'created_time')

class CategoryDetailSerializer(CategorySerializer):
    posts = serializers.SerializerMethodField('paginated_posts')

    def paginated_posts(self, obj):
        posts = obj.post_set.filter(status=Post.STATUS_NORMAL)
        paginator = pagination.PageNumberPagination()
        request = self.context['request']
        page = paginator.paginate_queryset(posts, request)
        serializers = PostSerializer(page, many=True, context={'request': request})
        return {
            'count': posts.count(),
            'results': serializers.data,
            'previous': paginator.get_previous_link(),
            'next': paginator.get_next_link(),
        }

    class Meta:
        model = Category
        fields = ('id', 'name', 'is_nav', 'created_time', 'posts')