from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField
from cloudinary.models import CloudinaryField

# Create your models here.
from django.db.transaction import on_commit

class User(AbstractUser):
    avatar = CloudinaryField('avatar', null=True)
    role = models.CharField(max_length=12, blank=True, null=True)
    is_approved = models.BooleanField(default=False)
    cccd = models.CharField(max_length=12, blank=True, null=True)

    def __str__(self):
        return self.username

class BaseModel(models.Model):
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True
        ordering = ['id']

# class Shipper(BaseModel):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     cccd = models.CharField(max_length=20)
#     is_approved = models.BooleanField(default=False)
#
#     def __str__(self):
#         return f"Shipper: {self.user.username}"

class Tag(BaseModel):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
# class Product(models.Model):
#     name = models.CharField(max_length=200)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     description = models.TextField()
#     tags = models.ManyToManyField(Tag)
#
#     def __str__(self):
#         return self.name


# class Order(models.Model):
#     STATUS_CHOICES = (
#         ('pending', 'Pending'),
#         ('shipping', 'Shipping'),
#         ('delivered', 'Delivered'),
#     )
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES)
#     note = models.TextField(blank=True, null=True)
#
#     def __str__(self):
#         return f"Order {self.id} by {self.user.username}"
#


class Category(BaseModel):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Course(BaseModel):
    name = models.CharField(max_length=100)
    description = RichTextField()
    image = models.ImageField(upload_to="courses/%Y/%m")
    category = models.ForeignKey(Category, on_delete=models.RESTRICT)
    tags = models.ManyToManyField('Tag')
    def __str__(self):
        return self.name

class Lesson(BaseModel):
    name = models.CharField(max_length=100)
    description = RichTextField()
    image = models.ImageField(upload_to="lessons/%Y/%m")
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    tags = models.ManyToManyField('Tag')

    def __str__(self):
        return self.name



class Interaction(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)

    class Meta:
        abstract = True

class Comment(Interaction):
    content = models.CharField(max_length=255)

class Like(Interaction):
    active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('user', 'lesson')

class Rating(Interaction):
    rate = models.SmallIntegerField(default=0)

class Setting(models.Model):
    name = models.CharField(max_length=256, blank=False, null=False, default="settings_name")
    value = models.CharField(max_length=256, blank=True, null=False, default='')