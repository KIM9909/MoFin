from django.shortcuts import render
from .models import Articles
from .serializers import ArticleSerializer
from rest_framework.viewsets import ModelViewSet

# Create your views here.
class ArticleViewSet(ModelViewSet):
    queryset = Articles.objects.all()
    serializer_class = ArticleSerializer