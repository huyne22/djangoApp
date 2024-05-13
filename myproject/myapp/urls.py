# myapp/urls.py

from django.urls import path, re_path, include
from myapp.admin import admin_site
from rest_framework import routers
from myapp import views
router = routers.DefaultRouter()
router.register('users', views.UserViewSet, basename="users")
router.register('shippers', views.ShipperViewSet, basename="shippers")
router.register('orders', views.OrderViewSet, basename="orders")
router.register('reviews', views.ReviewViewSet, basename="reviews")
router.register('auctions', views.AuctionViewSet, basename="auctions")

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin_site.urls),
    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),
]
