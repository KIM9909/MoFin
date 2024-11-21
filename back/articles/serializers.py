from rest_framework import serializers
from .models import Articles, Comment

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

# ArticleSerializer에서 댓글을 포함하도록 설정
class ArticleSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    user = serializers.SerializerMethodField()  # 추가

    class Meta:
        model = Articles
        fields = ['id', 'title', 'content', 'comments', 'created_at', 'updated_at', 'user']

    def get_user(self, obj):
        # 게시글 작성자 정보 반환
        return {
            'id': obj.user.id,
            'username': obj.user.username,
            'nickname': obj.user.nickname
        }