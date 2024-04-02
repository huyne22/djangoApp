from django.shortcuts import render
from rest_framework import viewsets, permissions, generics, status,parsers
from rest_framework.response import Response
from .models import Category, Course, Tag, Lesson, User, Comment, Like
from .serializer import CategorySerializer, CourseSerializer, LessonSerializer, UserSerializer, CommentSerializer, LessonSerializerDetail
from .paginator import CoursePaginator
from rest_framework.decorators import action
from .perms import OwnerPermission


# Create your views here.
class CategoryViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CourseViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CoursePaginator
    # permission_classes = [permissions.IsAuthenticated]

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


class UserViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = User.objects.all()
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
