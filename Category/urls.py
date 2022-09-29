from django.urls import path
from .views import *
urlpatterns = [
    path("category",category_list,name='category'),
    path("add_category",category_add,name='add_category'),
    path("category_delete/<int:id>",category_delete,name='category_delete'),

    path("sub_category_list",sub_category,name='sub_category_list'),

    path("sub_category/<int:id>",sub_category_list,name='sub_category'),
    path("add_sub_category",sub_category_add,name='add_sub_category'),
    path("sub_category_delete/<int:id>",sub_category_delete,name='sub_category_delete'),
]