from django.db import models


class Publication(models.Model):
    title = models.CharField(max_length=255)
    # contributors = models.ManyToManyField(User)
    code_url = models.CharField(max_length=255)
    arXiv_url = models.CharField(max_length=255)


class File(models.Model):
    type = models.CharField(max_length=255, default='')
    path = models.CharField(max_length=255, default='')
    url = models.CharField(max_length=255, default='')
    size = models.IntegerField(default=0)
    publication = models.OneToOneField(Publication, on_delete=models.CASCADE)
