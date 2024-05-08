# myapp/urls.py

from django.urls import path, re_path, include
from .admin import admin_site
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('categories', views.CategoryViewSet, basename="categories")
router.register('courses', views.CourseViewSet, basename="courses")
router.register('lessons', views.LessonViewSet, basename="lessons")
router.register('users', views.UserViewSet, basename="users")
router.register('comments', views.CommentViewSet, basename="comments")
# router.register('shippers', views.ShipperViewSet, basename="shippers")
urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin_site.urls),
    path('login/', views.LoginClass.as_view(), name='login'),
    path('signup/', views.SignupClass.as_view(), name='signup'),
    path('user-view/', views.ViewUser.as_view(), name='user-view'),
    path('create_order/', views.CreateOrderView.as_view(), name='create_order'),
    path('settings/', views.SettingsView.as_view()),

    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),
]
