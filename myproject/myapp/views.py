import cloudinary.uploader
from oauth2_provider.oauth2_validators import AccessToken
from rest_framework.parsers import FormParser, JSONParser
from rest_framework import viewsets, permissions, generics, status, parsers
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User,Shipper,Order,Review, Auction
from .serializer import UserSerializer, ShipperSerializer, OrderSerializer, ReviewSerializer,AuctionSerializer
from rest_framework.decorators import action

# Create your views here.

class UserViewSet(viewsets.ViewSet, generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    parser_classes = (FormParser, parsers.MultiPartParser, JSONParser)
    permission_classes = [permissions.IsAuthenticated]

    @action(methods=['post'], url_path="logout", detail=False)
    def logout(self, request):
        authorization_header = request.META.get('HTTP_AUTHORIZATION')

        if authorization_header:
            token = authorization_header.split()[1]
            try:
                access_token = AccessToken.objects.get(token=token)
                access_token.delete()
                return Response({'message': 'Logout successful'}, status=200)
            except AccessToken.DoesNotExist:
                return Response({'error': 'Invalid token'}, status=400)
        else:
            return Response({'error': 'Authorization header missing'}, status=400)

    def get_permissions(self):
        if self.action.__eq__('get_current'):
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    @action(methods=['get'], url_path="current", detail=False)
    def get_current(self, request):
        return Response(UserSerializer(request.user).data, status=status.HTTP_200_OK)

    @action(methods=['put'], url_path="update", detail=False)
    def update_current_user(self, request):
        if 'avatar' in request.data:
            user = request.user
            user.avatar = request.data['avatar']
            user.save()
            return Response({"message": "Avatar updated successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "No 'avatar' provided"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'])
    def delete_user(self, request, pk=None):
        try:
            user = self.get_object()
            # Kiểm tra quyền của người dùng
            if request.user.is_authenticated:
                if request.user.user_type == "admin":  # Kiểm tra nếu người dùng hiện tại là admin
                    # Kiểm tra nếu tài khoản cần xóa không phải là tài khoản admin
                    if not user.user_type == "admin":
                        user.delete()
                        return Response({"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
                    else:
                        return Response({"error": "Cannot delete admin account"}, status=status.HTTP_403_FORBIDDEN)
                else:
                    return Response({"error": "You do not have permission to delete users"},
                                    status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({"error": "You are not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ShipperViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Shipper.objects.all()
    serializer_class = ShipperSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        queryset = self.get_queryset()
        serializer = ShipperSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        data = request.data.copy()
        user = request.user
        avatar_file = None  # Khởi tạo biến avatar_file
        if 'avatar' in request.data:
            avatar_file = request.data['avatar']
        # Lấy tệp ảnh từ formData
        cccd = request.data.get('cccd')# Lấy thông tin cccd từ formData

        # Cập nhật user_type thành 'shipper'
        user.user_type = "shipper"
        user.save()  # Lưu lại đối tượng người dùng

        # Tạo hoặc cập nhật một đối tượng Shipper
        shipper, created = Shipper.objects.get_or_create(user=user)
        shipper.cccd = cccd
        shipper.avatar = "huy"
        if avatar_file:
            # Tải tệp ảnh lên Cloudinary và nhận URL của ảnh từ Cloudinary
            cloudinary_response = cloudinary.uploader.upload(avatar_file)
            cloudinary_url = cloudinary_response['secure_url']
            shipper.avatar = cloudinary_url  # Gán URL của ảnh vào trường avatar
            user.avatar = cloudinary_url

            # Lưu đối tượng Shipper
        shipper.save()
        user.save()

        # Serialize đối tượng Shipper và trả về dữ liệu
        serializer = ShipperSerializer(shipper)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['delete'])
    def delete_shipper(self, request, pk=None):
        try:
            shipper = self.get_object()
            shipper.delete()
            return Response({"message": "Shipper deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Shipper.DoesNotExist:
            return Response({"error": "Shipper not found"}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'])
    def shipper_display(self, request, pk=None):
        try:
            # Lấy thông tin về shipper
            shipper_instance = Shipper.objects.get(id=pk)
            shipper_data = ShipperSerializer(shipper_instance).data

            # Lấy đánh giá của shipper
            reviews = Review.objects.filter(shipper=shipper_instance)
            review_data = ReviewSerializer(reviews, many=True).data

            # Bổ sung thông tin đánh giá vào dữ liệu của shipper
            shipper_data['reviews'] = review_data

        except Shipper.DoesNotExist:
            return Response({"error": "Shipper not found"}, status=status.HTTP_404_NOT_FOUND)

        # Kiểm tra quyền truy cập
        if not request.user.user_type == "admin":
            return Response({"error": "You do not have permission to view shippers."},
                            status=status.HTTP_403_FORBIDDEN)

        # Xác nhận shipper và lưu
        shipper_instance.is_confirmed = True
        shipper_instance.save()
        # Serialize shipper đã được xác nhận và trả về dữ liệu
        return Response(shipper_data)

    @action(detail=True, methods=['post'])
    def confirm_shipper(self, request, pk=None):
        try:
            shipper = self.get_object()

        except Shipper.DoesNotExist:
            return Response({"error": "Shipper not found"}, status=status.HTTP_404_NOT_FOUND)

            # Perform permission checks here, if needed
        if not request.user.user_type == "admin":
            return Response({"error": "You do not have permission to confirm shippers."},
                            status=status.HTTP_403_FORBIDDEN)

        shipper.is_confirmed = True
        shipper.save()  # Lưu lại đối tượng Shipper
        serializer = ShipperSerializer(shipper)
        return Response(serializer.data)
class OrderViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    def list(self, request):
        queryset = self.queryset.filter(user=request.user)
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data)

        # orders = Order.objects.filter(active=True)
        # serializer = OrderSerializer(orders, many=True)
        # return Response(serializer.data)

    def create(self, request):
        data = request.data.copy()
        data['user'] = request.user.id
        # user_id = request.user.id
        # d = request.data
        # o = Order.objects.create(title=d['title'],
        #                          description=d['description'],
        #                          )

        serializer = OrderSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def confirm_is_completed(self, request, pk=None):
        try:
            order = self.get_object()
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        # Perform permission checks here
        if request.user.user_type != "shipper":
            return Response({"error": "Only shippers can confirm orders as completed."},
                            status=status.HTTP_403_FORBIDDEN)

        # Ensure the shipper confirming the order is the assigned shipper
        if order.shipper != request.user.shipper:
            return Response({"error": "You are not assigned to this order."},
                            status=status.HTTP_403_FORBIDDEN)

        order.is_completed = True
        order.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def confirm_shipper_order(self, request, pk=None):
        order = self.get_object()
        auctions = Auction.objects.filter(order=order)

        if auctions.exists():
            # Lấy shipper có giá bid cao nhất
            highest_bid_auction = auctions.order_by('-bid_price').first()

            # Gán shipper cho đơn hàng
            order.shipper = highest_bid_auction.shipper
            order.save()

            serializer = OrderSerializer(order)
            return Response(serializer.data)
        else:
            return Response({"error": "No shipper has placed a bid for this order"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def order_not_auction(self, request):
        try:
            # Lấy danh sách các ID đơn hàng đã được shipper đấu giá từ Auction
            orders_auctioned = Auction.objects.values_list('order_id', flat=True)

            # Lọc các đơn hàng chưa được đấu giá bằng cách loại bỏ các ID đã được shipper đấu giá
            orders_not_auction = Order.objects.exclude(id__in=orders_auctioned)

            if not request.user.user_type == "admin":
                return Response({"error": "You do not have permission to confirm shippers."},
                                status=status.HTTP_403_FORBIDDEN)

            # Serialize thông tin các đơn hàng
            serializer = OrderSerializer(orders_not_auction, many=True)
            return Response(serializer.data)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ReviewViewSet(viewsets.ViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def list(self, request):
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        data = request.data.copy()
        data['user'] = request.user.id
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AuctionViewSet(viewsets.ViewSet):
    queryset = Auction.objects.all()
    serializer_class = AuctionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):
        data = request.data.copy()
        data['shipper'] = request.user.shipper.id
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            shipper = request.user.shipper
            if shipper.is_confirmed:
                serializer.save(shipper=shipper)
                # Kiểm tra xem đơn hàng có mở cho việc đấu giá không
                # order_id = serializer.validated_data.get('order')
                order_id = data.get('order')
                if Order.objects.filter(id=order_id, is_completed=False).exists():
                    serializer.save(shipper=request.user.shipper)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response({"error": "This order is not open for bidding."},
                                    status=status.HTTP_400_BAD_REQUEST)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({"error": "This shipper is not confirmed by admin."},
                                status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        queryset = self.queryset.filter(order__user=request.user)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
class UserRegistrationView(APIView):
    serializer_class = UserSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
