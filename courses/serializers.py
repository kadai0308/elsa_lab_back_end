from user.serializers import UserSerializer
from .models import Course, Content, Lecture, File
from rest_framework import serializers


class FileSerializer(serializers.ModelSerializer):

    class Meta:
        model = File
        fields = ('id', 'title', 'size', 'type', 'path', 'url')


class LectureSerializer(serializers.ModelSerializer):
    files = FileSerializer(source='file_set', required=False, many=True)

    class Meta:
        model = Lecture
        fields = ('id', 'title', 'description', 'lecture_number', 'files')


class ContentSerializer(serializers.ModelSerializer):
    lectures = LectureSerializer(
        source='lecture_set',
        required=False,
        many=True)
    TAs = UserSerializer(source='tas', required=True, many=True)

    class Meta:
        model = Content
        fields = (
            'id', 'year', 'location',
            'course_no', 'time', 'season',
            'lectures', 'TAs')


class CourseSerializer(serializers.ModelSerializer):
    contents = ContentSerializer(
        source='content_set',
        required=False,
        many=True)

    class Meta:
        model = Course
        fields = ('id', 'title', 'contents', 'description')
