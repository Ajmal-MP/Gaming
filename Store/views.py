from django.shortcuts import render,get_object_or_404,redirect
from Category.models import Categories,SubCategories
from Product.models import Product
from Cart.models import CartItem,Cart
from Cart.views import _cart_id
import re
from django.core.paginator import Paginator

# Create your views here.
def store(request,category_slug = None ,sub_category_slug = None):
    categories = None
    sub_categories = None
    product = None
    filter_type = None    
    if 'query' in request.GET:
        query = request.GET.get('query')
        if query:
            product = Product.objects.filter(product_name__icontains = query)
            paginator = Paginator(product, 10)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            product_count = product.count()
        else:
            return redirect(store)
    elif category_slug != None and sub_category_slug == None:
        categories = get_object_or_404(Categories,slug = category_slug)
        product = Product.objects.filter(category_id = categories,is_active = True) 
        paginator = Paginator(product, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        product_count = product.count()
        filter_type = 'category'


        if request.method == 'POST':
            val=request.POST.get('value')
            val = re.findall("\d+", val) # code to get all inigers from string
            products = Product.objects.filter(category_id = categories,is_active = True).order_by('price') 
            paginator = Paginator(product, 10)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            min_price = int(val[0])
            max_price = int(val[1]) 
            product=[]
            for item in products:
                if int(item.price) >= min_price and int(item.price) <= max_price:
                    product.append(item)
            product_count = len(product)
            paginator = Paginator(product, 10)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            

    elif sub_category_slug != None and category_slug != None:
        sub_categories = get_object_or_404(SubCategories,slug = sub_category_slug)
        product = Product.objects.filter(subcategory_id = sub_categories, is_active = True)
        paginator = Paginator(product, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        product_count = product.count()
        filter_type = 'sub_category'
        if request.method == 'POST':
            val=request.POST.get('value')
            val = re.findall("\d+", val) # code to get all inigers from string
            products = Product.objects.filter(subcategory_id = sub_categories, is_active = True).order_by('price') 
            min_price = int(val[0])
            max_price = int(val[1]) 
            product=[]
            for item in products:
                if int(item.price) >= min_price and int(item.price) <= max_price:
                    product.append(item)
            product_count = len(product)
            paginator = Paginator(product, 10)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
    else:
        product = Product.objects.all().filter(is_active = True)
        paginator = Paginator(product, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        product_count = product.count()
    context = {
        'products': product,
        'product_count':product_count,
        'filter_type':filter_type,
        'page_obj':page_obj
    }
    return render(request,'UserSide/store.html',context)


def product_details(request,cat_slug,sub_cat_slug,product_slug):
    try:
        product = Product.objects.filter(subcategory_id__slug = sub_cat_slug, slug = product_slug)
    except Exception as e:
        raise e

    context={
        'product':product,
    }

    return render(request,'UserSide/product-detail.html',context)


def brand_filtered(request,brand):
    product = Product.objects.filter(brand = brand,is_active = True)
    context={
        'products':product
    }
    return render(request,'UserSide/store.html',context)



def filter(request):
    val=request.POST.get('value')
    number = re.findall("\d+", val)
    print(number)
    return redirect(store)