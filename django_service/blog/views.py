from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Article, User
from .producer import publish
from .serializers import ArticleSerializer
import random


class BlogView(viewsets.ViewSet):
    def list(self, request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = ArticleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        publish('article_created', serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        blog = blog.objects.get(id=pk)
        serializer = ArticleSerializer(instance=blog, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        publish('article_updated', serializer.data)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, pk=None):
        blog = blog.objects.get(id=pk)
        blog.delete()
        publish('article_deleted', pk)
        return Response(status=status.HTTP_204_NO_CONTENT)


class RandomUserView(APIView):
    def get(self, _):
        users = User.objects.all()
        user = random.choice(users)
        return Response({
            'id': user.id
        })