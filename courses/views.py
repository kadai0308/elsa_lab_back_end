# from django.shortcuts import render
from rest_framework.response import Response
from django.contrib import auth
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .models import Course, Content, Lecture, File
from elsa_lab_django.settings import DOMAIN
import os
import base64

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework_jwt.authentication import (
    BaseJSONWebTokenAuthentication, JSONWebTokenAuthentication
)

from .serializers import CourseSerializer, ContentSerializer, LectureSerializer, FileSerializer


class CourseList(APIView, JSONWebTokenAuthentication):
    """
    API endpoint that allows users to be viewed or edited.
    """

    def get(self, request, format=None):
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            path = './courses/course_data/{}'.format(serializer.data['title'])
            if not os.path.exists(path):
                os.makedirs(path)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseDetail(APIView, JSONWebTokenAuthentication):
    """
    Retrieve, update or delete a snippet instance.
    """

    def get(self, request, course_id, format=None):
        course = Course.objects.get(id=course_id)
        serializer = CourseSerializer(course)
        return Response(serializer.data)

    def put(self, request, course_id, format=None):
        course = Course.objects.filter(id=course_id)
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            course.update(**request.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, course_id, format=None):
        course = Course.objects.get(id=course_id)
        course.delete()
        if Course.objects.filter(id=course_id).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)

class ContentList(APIView, JSONWebTokenAuthentication):
    """
    API endpoint that allows users to be viewed or edited.
    """

    def get(self, request, course_id, format=None):
        course = Course.objects.get(id=course_id)
        contents = course.content_set.all()
        serializer = ContentSerializer(contents, many=True)
        return Response(serializer.data)

    def post(self, request, course_id, format=None):
        course = Course.objects.get(id=course_id)
        serializer = ContentSerializer(data=request.data)
        request.data.pop('users')
        request.data.pop('ta_names')
        user_ids = request.data.pop('ta_ids')
        users = []
        for id in user_ids:
            user = User.objects.get(id=id)
            users.append(user)
        if serializer.is_valid():
            content = course.content_set.create(**request.data)
            content.tas.set(users)
            path = './courses/course_data/{}/{}'.format(course.title, content.year)
            if not os.path.exists(path):
                os.makedirs(path)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContentDetail(APIView, JSONWebTokenAuthentication):
    """
    Retrieve, update or delete a snippet instance.
    """

    def get(self, request, course_id, content_id, format=None):
        content = Content.objects.get(id=content_id)
        serializer = ContentSerializer(content)
        return Response(serializer.data)

    def put(self, request, course_id, content_id, format=None):
        content = Content.objects.filter(id=content_id)
        request.data.pop('users')
        request.data.pop('TAs')
        request.data.pop('lectures')
        request.data.pop('ta_names')
        user_ids = request.data.pop('ta_ids')
        print (request.data)
        users = []
        for id in user_ids:
            user = User.objects.get(id=id)
            users.append(user)
        content[0].tas.set(users)
        content.update(**request.data)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, course_id, content_id, format=None):
        content = Content.objects.get(id=content_id)
        content.delete()
        if Content.objects.filter(id=content_id).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)


class LectureList(APIView, JSONWebTokenAuthentication):
    """
    API endpoint that allows users to be viewed or edited.
    """

    def get(self, request, course_id, content_id, format=None):
        content = Content.objects.get(id=content_id)
        lectures = content.lecture_set.all()
        serializer = LectureSerializer(lectures, many=True)
        return Response(serializer.data)

    def post(self, request, course_id, content_id, format=None):
        files = request.data.pop('files')
        content = Content.objects.get(id=content_id)
        course = content.course
        lecture_number = content.lecture_set.count() + 1
        request.data['lecture_number'] = lecture_number
        serializer = LectureSerializer(data=request.data)
        if serializer.is_valid():
            path = './courses/course_data/{}/{}/lecture{:0>2}'.format(
                course.title, content.year, lecture_number)
            if not os.path.exists(path):
                os.makedirs(path)
            lecture = content.lecture_set.create(**request.data)
            LectureList.new_file(lecture, path, files)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def new_file(lecture, path, files):
        for file in files:
            # 跳掉已經存在的 file
            if file.get('id', False):
                continue
            file_path = LectureList.write_file(path, file['title'], file['data'])
            file.pop('preview')
            file.pop('data')
            file['url'] = DOMAIN + '/static/' + '/'.join(file_path.split('/')[3:])
            file['path'] = file_path
            lecture.file_set.create(**file)

    @staticmethod
    def write_file(path, title, data):
        main_data = data.split(',')[-1]
        data = bytes(main_data, encoding='utf8')
        path = path + '/' + title
        with open(path, 'wb') as f:
            f.write(base64.decodebytes(data))
        return path


class LectureDetail(APIView, JSONWebTokenAuthentication):
    """
    Retrieve, update or delete a snippet instance.
    """

    def get(self, request, course_id, content_id, lecture_id, format=None):
        lecture = Lecture.objects.get(id=lecture_id)
        serializer = LectureSerializer(lecture)
        return Response(serializer.data)

    def put(self, request, course_id, content_id, lecture_id, format=None):
        lecture = Lecture.objects.filter(id=lecture_id)
        files = request.data.pop('files')
        content = Content.objects.get(id=content_id)
        course = content.course
        lecture_number = lecture[0].lecture_number
        serializer = LectureSerializer(data=request.data)
        if serializer.is_valid():
            path = './courses/course_data/{}/{}/lecture{:0>2}'.format(
                course.title, content.year, lecture_number)
            if not os.path.exists(path):
                os.makedirs(path)
            lecture.update(**request.data)
            LectureList.new_file(lecture[0], path, files)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, course_id, content_id, lecture_id, format=None):
        lecture = Lecture.objects.get(id=lecture_id)
        lecture.delete()
        if Lecture.objects.filter(id=lecture_id).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)


class FileDetail(APIView, JSONWebTokenAuthentication):
    """
    Retrieve, update or delete a snippet instance.
    """

    def get(self, request, file_id, format=None):
        file = File.objects.get(id=file_id)
        serializer = FileSerializer(file)
        return Response(serializer.data)

    def put(self, request, content_id, format=None):
        pass

    def delete(self, request, file_id, format=None):
        file = File.objects.filter(id=file_id)
        file.delete()
        if File.objects.filter(id=file_id).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)
