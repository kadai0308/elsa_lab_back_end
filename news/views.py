from .models import News
from .serializers import NewsSerializer
import logging
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.authentication import (
    BaseJSONWebTokenAuthentication, JSONWebTokenAuthentication
)

class NewsList(APIView, JSONWebTokenAuthentication):

    def get(self, request, format=None):
        # order by query params
        news = News.get_all_news(**request.query_params)
        serializer = NewsSerializer(news, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        is_created, result = News.create_news(request.data)
        if not is_created:
            print("Error: {}".format(result))
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
        return Response(result, status=status.HTTP_201_CREATED)
        

class NewsDetail(APIView, JSONWebTokenAuthentication):

    def get(self, request, news_id):
        news = News.get_news(news_id)
        serializer = NewsSerializer(news)
        return Response(serializer.data)

    def put(self, request, news_id):
        is_updated, result = News.update_news(news_id, request.data)
        if not is_updated:
            print("Error: {}".format(result))
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
        return Response(result, status=status.HTTP_201_CREATED)

    def delete(self, request, news_id):
        News.delete_news(news_id)
        if News.objects.filter(id=news_id).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
            print("Error: {}".format(result))
        return Response(status=status.HTTP_202_ACCEPTED)