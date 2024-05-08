from rest_framework.validators import UniqueValidator

from .models import Category, Course, Lesson, Tag, User, Comment
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

class BaseSerializer(ModelSerializer):
    image = serializers.SerializerMethodField(source='image')
    tags = TagSerializer(many=True)

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image:
            if request:
                return request.build_absolute_uri("/static/%s" % obj.image.name)
            return "/%s" % obj.image.name

class CourseSerializer(BaseSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class LessonSerializer(BaseSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'name', 'description', 'image', 'created_date', 'updated_date', 'course']

class LessonSerializerDetail(LessonSerializer):
    like = serializers.SerializerMethodField()

    def get_like(self, lesson):
        request = self.context.get('request')
        if request.user.is_authenticated:
            return lesson.like_set.filter(active=True, user=request.user).exists()

    class Meta:
        model = LessonSerializer.Meta.model
        fields = LessonSerializer.Meta.fields + ['like']


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        required=True,
        max_length=32,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    first_name = serializers.CharField(
        required=True,
        max_length=32,
    )
    last_name = serializers.CharField(
        required=True,
        max_length=32,
    )
    password = serializers.CharField(
        required=True,
        min_length=8,
        write_only=True
    )

    def create(self, validated_data):
        password = validated_data.pop('password',None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    class Meta:
        model = User
        fields = ['token', 'username','password','first_name',
                  'last_name',
                  'email','id']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content']

# class ShipperSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Shipper
#         fields = '__all__'