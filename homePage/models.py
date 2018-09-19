from django.db import models
from elsa_lab_django.settings import DOMAIN

class HomeCoverImage(models.Model):
    image_url = models.URLField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @staticmethod
    def get_all_cover_image_url():
        return HomeCoverImage.objects.all().order_by('created_at')

    @staticmethod
    def create_cover_image(data):
        from .serializers import HomeCoverImage

        serializer = HomeCoverImage(data=data)
        if serializer.is_valid():
            serializer.save()
            return (True, serializer.data)
        print(serializer.errors)
        return (False, serializer.errors)
