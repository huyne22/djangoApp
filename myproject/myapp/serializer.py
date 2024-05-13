from .models import User,Shipper,Order,Review,Auction
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'avatar', 'user_type', 'password']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def get_avatar(self, obj):
        if obj.user.avatar:
            return obj.user.avatar.url
        return None

    # if obj.avatar:
    #     return obj.avatar.url
    # return None
class ShipperSerializer(ModelSerializer):
    class Meta:
        model = Shipper
        fields = ['id', 'user', 'avatar', 'cccd', 'is_confirmed']

class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user', 'title', 'description', 'shipper', 'is_completed']

class ReviewSerializer(ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'user', 'shipper', 'rating', 'comment']

class AuctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auction
        fields = ['id', 'order', 'shipper', 'bid_price']
