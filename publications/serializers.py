from rest_framework import serializers
from .models import Publication, File


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ('id', 'size', 'type', 'url')


class PublicationSerializer(serializers.ModelSerializer):
    files = FileSerializer(source='file', required=False, many=False)

    class Meta:
        model = Publication
        fields = ('id', 'title', 'code_url', 'arXiv_url', 'files')
