from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField
# Create your models here.

class User(AbstractUser):
    email = models.EmailField(unique=True)
    avatar = CloudinaryField('avatar', null=True)
    user_type = models.CharField(max_length=20, choices=(
        ('shipper', 'Shipper'),
        ('admin', 'Admin'),
        ('customer', 'Customer'),
    ), default='customer')

    def save(self, *args, **kwargs):
        # Kiểm tra xem người dùng đã tồn tại trong cơ sở dữ liệu chưa
        if not self.pk:
            # Nếu không, tức là người dùng đang được tạo mới, hãy băm mật khẩu
            self.password = make_password(self.password)
        # Gọi phương thức save của lớp cha
        super().save(*args, **kwargs)

class BaseModel(models.Model):
    # created_date = models.DateField(auto_now_add=True)
    # updated_date = models.DateField(auto_now=True)
    # active = models.BooleanField(default=True)
    class Meta:
        abstract = True
        ordering = ['id']

class Shipper(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = CloudinaryField('avatar')
    cccd = models.CharField(max_length=20)
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    shipper = models.ForeignKey(Shipper, on_delete=models.SET_NULL, null=True, blank=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shipper = models.ForeignKey(Shipper, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()

    def __str__(self):
        return f"Review for {self.shipper.user.username}"

class Auction(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    shipper = models.ForeignKey(Shipper, on_delete=models.CASCADE)
    bid_price = models.IntegerField()

    def __str__(self):
        return f"Auction for order: {self.order.title} - Shipper: {self.shipper.username} - Bid Price: {self.bid_price}"

