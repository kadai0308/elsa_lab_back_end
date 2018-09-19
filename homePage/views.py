from .models import HomeCoverImage
from .serializers import HomeCoverImageSerializer
import logging
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.authentication import (
    BaseJSONWebTokenAuthentication, JSONWebTokenAuthentication
)

class HomeCoverImageList(APIView, JSONWebTokenAuthentication):

    def get(self, request, format=None):
        cover_image_urls = HomeCoverImage.get_all_cover_image_url()
        serializer = HomeCoverImageSerializer(cover_image_urls, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        is_created, result = HomeCoverImage.create_cover_image(request.data)
        if not is_created:
            print("Error: {}".format(result))
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
        return Response(result, status=status.HTTP_201_CREATED)