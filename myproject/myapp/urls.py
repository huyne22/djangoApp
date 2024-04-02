# myapp/urls.py

from django.urls import path, re_path, include
from .admin import admin_site
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('categories', views.CategoryViewSet, basename="categories")
router.register('courses', views.CourseViewSet, basename="courses")
router.register('lessons', views.LessonViewSet, basename="lesson")
router.register('users', views.UserViewSet, basename="users")
router.register('comments', views.CommentViewSet, basename="comments")
urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin_site.urls),
    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),
]
