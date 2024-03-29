"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import ckeditor_uploader
from django.contrib import admin
from django.urls import path, re_path, include
from myapp.admin import admin_site
from rest_framework import routers
from myapp import views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Course API",
        default_version='v1',
        description="APIs for CourseApp",
        contact=openapi.Contact(email="luonghuy148894@gmail.com"),
        license=openapi.License(name="luongvanhuy"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = routers.DefaultRouter()
router.register(r'categories', views.CategoryViewSet, basename='categories')
# router.register('categories', views.CategoryViewSet, basename="categories")
router.register('courses', views.CourseViewSet, basename="courses")
router.register('lessons', views.LessonViewSet, basename="lessons")
router.register('users', views.UserViewSet, basename="users")

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin_site.urls),
    path('o/', include('oauth2_provider.urls',
    namespace='oauth2_provider')),
    # path('categories/add_category/', views.CategoryViewSet.as_view({'post': 'add_category'}), name='add-category'),

    re_path(r'^ckeditor/',include('ckeditor_uploader.urls')),
    path("__debug__/", include("debug_toolbar.urls")),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
    schema_view.without_ui(cache_timeout=0),
    name='schema-json'),
    re_path(r'^swagger/$',
    schema_view.with_ui('swagger', cache_timeout=0),
    name='schema-swagger-ui'),
    re_path(r'^redoc/$',
    schema_view.with_ui('redoc', cache_timeout=0),
    name='schema-redoc')
]