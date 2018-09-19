from django.db import models
from elsa_lab_django.settings import DOMAIN
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from enum import Enum
import os
import requests


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# student enum
studentType = Enum('studentType', 'course_student College Master PHD Teacher Alumni')
studentTypeChoices = tuple([(str(i.value), i.name) for i in studentType])


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    studentType = models.CharField(max_length=1, choices=studentTypeChoices)
    nick_name = models.CharField(max_length=255)
    name = models.CharField(max_length=255, default='')
    pictureUrl = models.URLField(max_length=200, default=DOMAIN + "/static/users_avaters/default.jpg")
    researchArea = models.TextField()
    selfIntro = models.TextField()
    student_id = models.CharField(max_length=255)

# !!! NEED TO BE REFACTORED !!!
@receiver(post_save, sender=Profile)
def save_user_profile(sender, instance, **kwargs):
    print(instance.pictureUrl)
    if not instance.pictureUrl or DOMAIN in instance.pictureUrl:
        return
    path = './user/avaters/users_avaters/{}'.format(instance.user.username)
    print(os.path.exists(path))
    if not os.path.exists(path):
        os.makedirs(path)
    with open(path + '/avater.jpg', 'wb') as f:
        img = requests.get(instance.pictureUrl, stream=True)
        for bits in img.iter_content(1024):
            if not bits:
                    break
            f.write(bits)
    newPicPath = (
        DOMAIN + "/static/users_avaters/{}/avater.jpg"
        .format(instance.user.username)
    )
    Profile.objects.filter(pk=instance.pk).update(pictureUrl=newPicPath)
