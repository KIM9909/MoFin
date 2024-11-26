from rest_framework import serializers
from .models import Article, Comment

# CommentSerializer에서 user 정보를 상세히 표시
class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()  # 사용자 정보를 포함하는 메소드 필드 추가

    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_at', 'article', 'user']
        read_only_fields = ['user']

    # user 필드를 확장하여 nickname과 username을 반환
    def get_user(self, obj):
        return {
            'id': obj.user.id,
            'username': obj.user.username,
            'nickname': obj.user.nickname,  # 추가된 필드: nickname
        }

class ArticleSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    user = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'comments', 'created_at', 
                 'updated_at', 'user', 'like_count', 'is_liked']

    def get_user(self, obj):
        return {
            'id': obj.user.id,
            'username': obj.user.username,
            'nickname': obj.user.nickname
        }

    def get_like_count(self, obj):
        return obj.like_users.count()

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.like_users.filter(id=request.user.id).exists()
        return False