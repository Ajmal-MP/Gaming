from django.urls import path

from Order.views import cash_on_delivery
from .views import *


urlpatterns = [
    path("product/",product_list,name='product'),
    path("add_product",add_product,name='add_product'),
    path("product_delete/<int:id>",product_delete,name='product_delete'),
    path("product_update/<int:id>",update_produect,name='product_update'),
    path("cash_on_delivery/<int:product_order_number>",cash_on_delivery,name='cash_on_delivery'),

    path("product_offer",product_offer,name='product_offer'),
    path("add-product-offer",add_product_offer,name='add-product-offer'),
    path("product_offer_delete/<int:id>",product_offer_delete,name='product_offer_delete'),



]