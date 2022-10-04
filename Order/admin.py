from django.contrib import admin
from .models import Order,OrderProduct,Payment,Address,Coupon,UserCoupon
# Register your models here.

admin.site.register(Order)
admin.site.register(OrderProduct)
admin.site.register(Payment)
admin.site.register(Address)
admin.site.register(Coupon)
admin.site.register(UserCoupon)

