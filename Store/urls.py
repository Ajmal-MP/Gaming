from django.urls import path
from .views import *
urlpatterns = [
    path("",store,name='store'),
    path("<slug:category_slug>/",store,name='product_by_category'),
    path("<slug:category_slug>/<slug:sub_category_slug>/",store,name='product_by_sub_category'),
    path("<slug:cat_slug>/<slug:sub_cat_slug>/<slug:product_slug>",product_details,name='product_detail'),
    path("/<str:brand>/",brand_filtered,name='brand_filtered'),
    path("filter",filter,name='filter'),

]