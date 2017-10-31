from django.contrib.auth.models import User
from .models import Profile
from rest_framework import serializers


# class ProfileSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Profile
#         fields = ('user', 'name')


# class UserSerializer(serializers.HyperlinkedModelSerializer):
#     profile = ProfileSerializer(read_only=True)
#     class Meta:
#         model = User
#         fields = ('url', 'username', 'email', 'groups', 'profile')

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            'name', 'studentType', 'pictureUrl',
            'researchArea', 'selfIntro'
        )


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'profile')
