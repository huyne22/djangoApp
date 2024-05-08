from django.contrib.auth import authenticate
from django.contrib.sites import requests
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View
from rest_framework import viewsets, permissions, generics, status, parsers
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView

from .models import Category, Course, Tag, Lesson, User, Comment, Like, Setting
from .serializer import CategorySerializer, CourseSerializer, LessonSerializer, UserSerializer, CommentSerializer, LessonSerializerDetail
from .paginator import CoursePaginator
from rest_framework.decorators import action
from .perms import OwnerPermission
import requests

# Create your views here.
class CategoryViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CourseViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CoursePaginator
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queries = self.queryset
        q = self.request.query_params.get('q')
        if q:
            queries = queries.filter(name__icontains=q)
        return queries

    @action(methods=['GET'], detail=True)
    def lessons(self, request, pk):
        l = self.get_object().lesson_set.filter(active=True)
        return Response(LessonSerializer(l, many=True, context={
            'request': request
        }).data, status=status.HTTP_200_OK)


class LessonViewSet(viewsets.ViewSet, generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializerDetail

    def get_permissions(self):
        if self.action in ['add_comment', 'like']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    @action(methods=["post"], url_path="comments", detail=True)
    def add_comment(self, request, pk):
        comment = Comment.objects.create(user=request.user, lesson=self.get_object(), content=request.data.get('content'))
        comment.save()
        return Response(CommentSerializer(comment, context={
            'request': request
        }).data, status=status.HTTP_201_CREATED)

    @action(methods=["get"], url_path="comments", detail=True)
    def get_comments(self, request, pk):
        comments = self.get_object().comment_set.all(active=True)
        return Response(CommentSerializer(comments, many=True).data, status=status.HTTP_200_OK)

    @action(methods=["post"], url_path="like", detail=True)
    def like(self, request, pk):
        like, create = Like.objects.get_or_create(user=request.user, lesson=self.get_object())
        if not create:
            like.active = not like.active
            like.save()

        return Response(LessonSerializerDetail(self.get_object(), context={
            'request': request
        }).data, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ViewSet, generics.ListAPIView, generics.CreateAPIView, generics.RetrieveAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    parser_classes = [parsers.MultiPartParser]

    def get_permissions(self):
        if self.action.__eq__('get_current'):
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    @action(methods=['get'], url_path="current", detail=False)
    def get_current(self, request):
        return Response(UserSerializer(request.user).data, status=status.HTTP_200_OK)


class CommentViewSet(viewsets.ViewSet, generics.DestroyAPIView, generics.UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [OwnerPermission]

# class ShipperViewSet(viewsets.ViewSet, generics.ListAPIView, generics.CreateAPIView, generics.RetrieveAPIView):
#     queryset = User.objects.filter(is_approved=False)
#     serializer_class = UserSerializer
#     parser_classes = [parsers.MultiPartParser]
#
#     def get_permissions(self):
#         if self.action in ['add_shippers']:
#             return [permissions.IsAuthenticated()]
#         return [permissions.AllowAny()]
#
#     @action(methods=["post"], url_path="shippers", detail=True)
#     def add_shippers(self, request, pk):
#         shipper = Shipper.objects.create(user=request.user)
#         shipper.save()
#         return Response(ShipperSerializer(shipper, context={
#             'request': request
#         }).data, status=status.HTTP_201_CREATED)

#test
class LoginClass(View):
    def get(self, request):
        return render(request, 'login/login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Send authentication request to OAuth2 Server
        token_url = 'http://127.0.0.1:8000/o/token/'
        token_data = {
            'grant_type': 'password',
            'username': username,
            'password': password,
            'client_id': 'gRhC8z5T5NNBiESCV0qo15r9z1YwVFUa6yzbKEnH',
            'client_secret': 'nulbEPeFKCpx73ooDyPYiQefRknkv8jaKbgAOnqhd2sf4zqSctmu4OyOpDfInpu8LaMCmrei5us7NF07qycchSQjYtKyYvPSQNK5XDyn5wjFaPMBVMb0O0I0IUnHZACl',
        }
        response = requests.post(token_url, data=token_data)
        if response.status_code == 200:
            # Authentication successful, return access token
            access_token = response.json().get('access_token')
            return JsonResponse({'access_token': access_token}, status=200)
        else:
            # Authentication failed
            return JsonResponse({'error': 'Login failed'}, status=401)

class SignupClass(View):
    def get(self, request):
        return render(request, 'signup/signup.html')

    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            return HttpResponse('Passwords do not match. Please try again.')

        # Check if username or email already exists
        if User.objects.filter(username=username).exists():
            return HttpResponse('Username already exists. Please choose a different one.')
        if User.objects.filter(email=email).exists():
            return HttpResponse('Email already exists. Please use a different one.')

        # Create new user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        return HttpResponse('Signup successful. You can now login.')

class CreateOrderView(View):
    def post(self, request):
        # Xử lý logic để tạo đơn hàng ở đây
        # Sau khi xử lý, trả về một JsonResponse để thông báo kết quả cho người dùng
        return JsonResponse({'message': 'Order created successfully'})
class ViewUser(View):
    def get(self,request):
        if not request.user.is_authenticated:
            return HttpResponse("Ban vui long dang nhap")
        else:
            return render(request, 'dashboard/dashboard.html')
class UserView(APIView):
    def post(self,request,format=None):
        print("Creating a user")

        user_data = request.data
        print(request.data)

        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid(raise_exception=False):
            user_serializer.save()

            return Response({"user": user_serializer.data}, status=200)
        return Response({"msg":"ERR"}, status=400)

class UserLoginView(APIView):
    def get(self,request,format=None):
        if request.user.is_authenticated == False or request.user.is_active == False:
            return Response("Invalid Credentials", status=403)

        user = UserSerializer(request.user)
        return Response(user.data, status=200)
    def post(self,request,format=None):
        # Xác thực người dùng
        print("Login Class")
        user_obj = User.objects.filter(email=request.data['username']).filter() or User.objects.filter(usename=request.data['username']).filter()
        if user_obj is not None:
            credentials = {
                'username': user_obj.username,
                'password': request.data['password']
            }
            user = authenticate(**credentials)

            if user and user.is_active:
                user_serializer = UserSerializer(user)
                return Response(user_serializer.data, status=200)
        return Response("Invalid Credentials", status=403)

class SettingsView(APIView):
    def get(self, request, format=None):
        settingsDict = {}
        #{"NAME":"VALUE", "NAME2":"VALUE2"}

        try:
            settingObjects = Setting.objects.all()

            for setting in settingObjects:
                settingsDict[setting.name] = setting.value

            return Response(settingsDict, status=200)

        except:
            return Response(status=404)

    def post(self, request, format=None):

        #This view we are going to create new settings in the DB

        #JSON Object: {"setings": [{"NAME":NAME, "VALUE":VALUE}, {"NAME":NAME, "VALUE":VALUE}]}
        settings = request.data['settings']
        bad_settings = []
        for setting in settings:
            try:
                new_setting = Setting(name=setting['NAME'], value=setting['VALUE'])
                new_setting.save()
            except:
                bad_settings.append(setting)

        if len(bad_settings) > 0:
            return Response({"INVALID SETTINGS": bad_settings}, status=200)

        else:
            return Response(status=200)