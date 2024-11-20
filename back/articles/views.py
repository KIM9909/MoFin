from django.shortcuts import render
from .models import Articles
from .serializers import ArticleSerializer
from rest_framework.viewsets import ModelViewSet

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication

class ArticleViewSet(ModelViewSet):
    queryset = Articles.objects.all()
    serializer_class = ArticleSerializer
    authentication_classes = [TokenAuthentication]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]