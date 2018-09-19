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
        username = request.data['username']
        resp_data = {}
        
        # error handle
        if not '@' in username:
            resp_data['type'] = 'error'
            resp_data['message'] = 'Account(Username) have to be email.'
            return JsonResponse(resp_data)

        # if user already existed
        if User.objects.filter(username=username).exists():
            resp_data['type'] = 'error'
            resp_data['message'] = 'Username already exists.'
            return JsonResponse(resp_data)

        accont_data = {
            'username': request.data['username'],
            'password': request.data.get('password', 'elsalab')
        }

        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_user(**accont_data)
            self.updateProfile(user.profile, request.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def updateProfile(self, profile, data):
        print(data)
        profile.name = data.get('name', '')
        profile.nick_name = data.get('nick_name', '')
        profile.pictureUrl = data.get('pictureUrl', '')
        profile.studentType = data.get('studentType', 'course_student')
        profile.researchArea = data.get('researchArea', '')
        profile.selfIntro = data.get('selfIntro', '')
        profile.student_id = data.get('student_id', '')
        profile.save()


class UserDetail(APIView, JSONWebTokenAuthentication):
    """
    Retrieve, update or delete a snippet instance.
    """

    def get(self, request, user_id, format=None):
        user = User.objects.get(id=user_id)
        # user, jwt = self.authenticate(request)
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
