# from django.shortcuts import render
from rest_framework.response import Response
from django.contrib import auth
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .models import Publication, File
from elsa_lab_django.settings import DOMAIN
import os
from os.path import splitext
import base64


from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework_jwt.authentication import (
    BaseJSONWebTokenAuthentication, JSONWebTokenAuthentication
)

from .serializers import PublicationSerializer


def create_and_write_file(publication, file):
    path = './publications/publications_file/{}'.format(publication.title)
    # fetch the data of uploaded file
    file_data = file.pop('data').split(',')[-1]
    # encoding to utf-8
    file_data = bytes(file_data, encoding='utf8')
    # extract extension
    filename, extension = splitext(file.pop('title'))
    # local file path ( file name )
    local_path = path + '/' + publication.title + extension
    # write file
    with open(local_path, 'wb') as f:
        f.write(base64.decodebytes(file_data))
    file.pop('preview')
    file['url'] = DOMAIN + '/static/' + '/'.join(local_path.split('/')[3:])
    file['path'] = local_path
    file['publication'] = publication
    File.objects.create(**file)


class PublicationList(APIView, JSONWebTokenAuthentication):
    """
    API endpoint that allows users to be viewed or edited.
    """

    def get(self, request, format=None):
        publications = Publication.objects.all()
        serializer = PublicationSerializer(publications, many=True)
        return Response(serializer.data)

    # upload file data format: base64
    def post(self, request, format=None):
        serializer = PublicationSerializer(data=request.data)
        data = request.data
        if serializer.is_valid():
            path = './publications/publications_file/{}'.format(serializer.data['title'])
            if not os.path.exists(path):
                os.makedirs(path)

            # front-end only allow upload one file
            file = data.pop('files')[0]
            # create Publication object
            p = Publication.objects.create(**data)
            # create and write file object
            create_and_write_file(p, file)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PublicationDetail(APIView, JSONWebTokenAuthentication):
    """
    Retrieve, update or delete a snippet instance.
    """

    def get(self, request, publication_id, format=None):
        publication = Publication.objects.get(id=publication_id)
        serializer = PublicationSerializer(publication)
        return Response(serializer.data)

    def put(self, request, publication_id, format=None):
        publication = Publication.objects.get(id=publication_id)
        data = request.data
        file = data.pop('files')[0]
        serializer = PublicationSerializer(data=request.data)
        print(serializer.is_valid())
        if serializer.is_valid():
            path = './publications/publications_file/{}'.format(serializer.data['title'])
            if not os.path.exists(path):
                os.makedirs(path)
            if hasattr(publication, 'file'):
                publication.file.delete()
            create_and_write_file(publication, file)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, publication_id, format=None):
        publication = Publication.objects.get(id=publication_id)
        publication.delete()
        if Publication.objects.filter(id=publication_id).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)


class FileDetail(APIView, JSONWebTokenAuthentication):
    def delete(self, request, publication_id, format=None):
        publication = Publication.objects.get(id=publication_id)
        publication.file.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
