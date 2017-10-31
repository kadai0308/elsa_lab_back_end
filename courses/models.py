from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_delete
from django.dispatch import receiver
import os

class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()


class Content(models.Model):
    year = models.IntegerField()
    season = models.CharField(max_length=255)
    time = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    course_no = models.CharField(max_length=255)
    tas = models.ManyToManyField(User)
    course = models.ForeignKey(Course, null=True)


class Lecture(models.Model):
    lecture_number = models.IntegerField()
    title = models.CharField(max_length=255)
    description = models.TextField()
    course_content = models.ForeignKey(Content, null=True)


class File(models.Model):
    title = models.CharField(max_length=255)
    size = models.IntegerField()
    type = models.CharField(max_length=255)
    path = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    lecture = models.ForeignKey(Lecture, null=True)


@receiver(pre_delete, sender=File)
def delete_local_file(sender, instance,  **kwargs):
    print(instance.path)
