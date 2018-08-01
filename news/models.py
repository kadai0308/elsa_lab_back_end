from django.db import models

# Create your models here.
class News(models.Model):
    

    title = models.CharField(max_length=255)
    description = models.TextField()
    content = models.TextField()
    image_url = models.URLField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @staticmethod
    def get_all_news(order=[]):
        return News.objects.all().order_by(*order)

    @staticmethod
    def get_news(news_id):
        return News.objects.get(id=news_id)

    @staticmethod
    def filter_by_attr(attr_dict):
        return News.objects.filter(**attr_dict)

    @staticmethod
    def create_news(data):
        # avoid circular import
        from .serializers import NewsSerializer

        serializer = NewsSerializer(data=data)
        print(data)
        if serializer.is_valid():
            serializer.save()
            return (True, serializer.data)
        print(serializer.errors)
        return (False, serializer.errors)

    @staticmethod
    def update_news(news_id, data):
        # avoid circular import
        from .serializers import NewsSerializer

        news = News.filter_by_attr({ 'id': news_id })
        serializer = NewsSerializer(data=data)
        if serializer.is_valid():
            news.update(**data)
            return (True, serializer.data)
        return (False, serializer.error)

    @staticmethod
    def delete_news(news_id):
        News.filter_by_attr({ 'id': news_id }).delete()

