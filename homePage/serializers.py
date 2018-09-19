from .models import HomeCoverImage
from rest_framework import serializers

class HomeCoverImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeCoverImage
        fields = ('image_url', 'created_at', 'updated_at')