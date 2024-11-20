from rest_framework import serializers
from .models import Articles, Comment

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_at', 'article', 'user']
        read_only_fields = ['user']

class ArticleSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)  # 관련 댓글 표시

    class Meta:
        model = Articles
        fields = ['id', 'title', 'content', 'comments', 'created_at', 'updated_at']
