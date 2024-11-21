from rest_framework.viewsets import ModelViewSet
from .models import Article, Comment
from .serializers import ArticleSerializer, CommentSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response

class ArticleViewSet(ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    authentication_classes = [TokenAuthentication]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        """게시글 작성 시 현재 로그인한 사용자를 작성자로 지정"""
        serializer.save(user=self.request.user)

class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [TokenAuthentication]

    @action(detail=False, methods=['get'], url_path='article/(?P<article_id>[^/.]+)')
    def article_comments(self, request, article_id=None):
        """특정 게시글의 댓글 목록을 반환하는 메서드"""
        comments = Comment.objects.filter(article_id=article_id)
        serializer = self.get_serializer(comments, many=True)
        return Response(serializer.data)

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        """댓글 작성 시 현재 로그인한 사용자를 작성자로 지정"""
        serializer.save(user=self.request.user)