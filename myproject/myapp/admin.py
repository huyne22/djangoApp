from django.contrib import admin
from .models import User, Shipper, Order, Review, Auction
from django.contrib.auth.models import Permission

class AppAdminSite(admin.AdminSite):
    site_header = "Hệ thống quản lý giao hàng"

    # def get_urls(self):
    #     return [
    #                    path('course-stats/', self.stats_view)
    #            ] + super().get_urls()
    #
    # def stats_view(self, request):
    #     stats = count_course_by_cate()
    #     return TemplateResponse(request, 'admin/stats_view.html',{
    #         'stats': stats
    #     })

# Register your models here.
# class CourseTagInlineAdmin(admin.TabularInline):
#     model = Course.tags.through

class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username','email','user_type','avatar']

class ShipperAdmin(admin.ModelAdmin):
    list_display = ['id', 'avatar','user_id','is_confirmed']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id','shipper_id','title','description','is_completed']

class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'shipper_id', 'rating', 'comment']
class AuctionAdmin(admin.ModelAdmin):
    list_display = ['id', 'order_id','shipper_id','bid_price']

admin_site = AppAdminSite(name="myapp")

admin_site.register(User,UserAdmin)
admin_site.register(Shipper,ShipperAdmin)
admin_site.register(Order,OrderAdmin)
admin_site.register(Review,ReviewAdmin)
admin_site.register(Auction,AuctionAdmin)
admin_site.register(Permission)
