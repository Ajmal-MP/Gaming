from django.urls import path
from .views import *
urlpatterns = [
    path("category",category_list,name='category'),
    path("category_offer",category_offer,name='category_offer'),
    path("add_category",category_add,name='add_category'),
    path("add-category-offer",add_category_offer,name='add-category-offer'),
    path("category_delete/<int:id>",category_delete,name='category_delete'),

    path("sub_category_list",sub_category,name='sub_category_list'),

    path("sub_category/<int:id>",sub_category_list,name='sub_category'),
    path("add_sub_category",sub_category_add,name='add_sub_category'),
    path("sub_category_delete/<int:id>",sub_category_delete,name='sub_category_delete'),
    path("category_offer_delete/<int:id>",category_offer_delete,name='category_offer_delete'),

    
]