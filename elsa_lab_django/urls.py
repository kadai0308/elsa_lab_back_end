"""elsa_lab_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url, include
from rest_framework import routers
from user import views
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
# from django.contrib import admin
import user.views as users
import courses.views as courses
import publications.views as publications

# router = routers.DefaultRouter()
# router.register(r'users', views.UserViewSet)

urlpatterns = [
    # url(r'^', include(router.urls)),
    # url(r'^api-auth/', include('rest_framework.urls',
    #     namespace='rest_framework')),
    url(r'^users$', users.UserList.as_view()),
    url(r'^user/(?P<user_id>[0-9]+)$', users.UserDetail.as_view()),
    url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^api-token-refresh/', refresh_jwt_token),
]

urlpatterns += (
    url(r'^publications$', publications.PublicationList.as_view()),
    url(r'^publications/(?P<publication_id>[0-9]+)$', publications.PublicationDetail.as_view()),
    url(r'^publications/(?P<publication_id>[0-9]+)/file$', publications.FileDetail.as_view()),
)

urlpatterns += (
    url(r'^courses$', courses.CourseList.as_view()),
    url(r'^courses/(?P<course_id>[0-9]+)$', courses.CourseDetail.as_view()),
    url(r'^courses/(?P<course_id>[0-9]+)/contents$', courses.ContentList.as_view()),
    url(r'^courses/(?P<course_id>[0-9]+)/contents/(?P<content_id>[0-9]+)$', courses.ContentDetail.as_view()),
    url(r'^courses/(?P<course_id>[0-9]+)/contents/(?P<content_id>[0-9]+)/lectures$', courses.LectureList.as_view()),
    url(r'^courses/(?P<course_id>[0-9]+)/contents/(?P<content_id>[0-9]+)/lectures/(?P<lecture_id>[0-9]+)$', courses.LectureDetail.as_view()),
)

urlpatterns += (
    url(r'^files/(?P<file_id>[0-9]+)$', courses.FileDetail.as_view()),
)