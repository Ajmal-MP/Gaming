from unicodedata import name
from django.urls import path
from .views import *
urlpatterns = [
 path('place_order/',place_order,name = 'place_order'),
 path('payments/',payments,name = 'payments'),
 path('payments_completed/',payments_completed,name = 'payments_completed'),
 path('user_orders',user_orders,name="user_orders"),
 path('admin_orders',admin_orders_list,name="admin_orders"),
 path('razor_pay',razor_pay,name="razor_pay"),
 path('admin_update_order/<int:id>',update_admin_order,name="update_admin_order"),
 path("cash_on_delivery/<int:id>",cash_on_delivery,name='cash_on_delivery'),
 path("cancel_order/<int:id>",cancel_order,name='cancel_order'),
 path("return_order/<int:id>",return_order,name='return_order'),
 path('coupon',coupon,name="coupon"),
 path('coupon_add',admin_add_coupon,name='admin_add_coupon'),
 path('admin_display_coupon',admin_display_coupon,name='admin_display_coupon'),
 path("coupon_delete/<int:id>",coupon_delete,name='coupon_delete'),
 path("coupon_update/<int:id>",coupon_update,name='coupon_update'),
]