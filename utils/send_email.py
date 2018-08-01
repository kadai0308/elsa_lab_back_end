from django.contrib.auth.models import User
from user.models import Profile
from courses.models import File
from django.core.mail import send_mail
import elsa_lab_django.settings as settings
import sys
import threading

def parse_users_email(user_ids):
    email_address = set()
    for id in user_ids:
        
        user = Profile.objects.get(nick_name=id[1:]).user
        email_address.add(user.username)
        
    return email_address

def parse_subject(message_data):
    message_type = message_data.get("message_type", "")
    if message_type == "course_file_comment_reply":
        file  = message_data["file"]
        file_title = file.title
        return "Elsa lab: You have been mentioned under {}".format(file_title)

def parse_message(message_type, link):
    if message_type == "course_file_comment_reply":
        return "You got new reply! Check it out: {}".format(link)

def send_email(message_data):
    email_address = parse_users_email(message_data["mentions"])
    email_subject = parse_subject(message_data)
    email_messaege = parse_message(message_data["message_type"], message_data["link"])
    send_mail(
        email_subject,
        email_messaege,
        settings.EMAIL_HOST_USER,
        email_address,
        fail_silently=False,
    )