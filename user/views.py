# from django.shortcuts import render
from rest_framework.response import Response
from django.contrib import auth
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework_jwt.authentication import (
    BaseJSONWebTokenAuthentication, JSONWebTokenAuthentication
)

from .models import Profile
from .serializers import UserSerializer
import os
import requests


class UserList(APIView, JSONWebTokenAuthentication):
    """
    API endpoint that allows users to be viewed or edited.
    """

    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        userData = {
            'username': request.data.pop('username'),
            'password': 'elsayoyo'
        }
        serializer = UserSerializer(data=userData)
        if serializer.is_valid():
            user = User.objects.create_user(**userData)
            self.updateProfile(user.profile, request.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def updateProfile(self, profile, data):
        profile.name = data['name']
        profile.pictureUrl = data['pictureUrl']
        profile.studentType = data['studentType']
        profile.researchArea = data['researchArea']
        profile.selfIntro = data['selfIntro']
        profile.save()


class UserDetail(APIView, JSONWebTokenAuthentication):
    """
    Retrieve, update or delete a snippet instance.
    """

    def get(self, request, user_id, format=None):
        user, jwt = self.authenticate(request)
        if user.id != user_id:
            # raise auth error
            pass
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, user_id, format=None):
        user, jwt = self.authenticate(request)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user_id, format=None):
        pass
