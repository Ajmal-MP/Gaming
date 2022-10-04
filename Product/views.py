from django.shortcuts import render,redirect
from .form import ProductForm
from .models import Product
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required 
from django.core.paginator import Paginator
# Create your views here.

@staff_member_required(login_url='admin_login')
def product_list(request):
    product=Product.objects.all()
    paginator = Paginator(product, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context={
        'product':product,
        'page_obj': page_obj
    }
    return render(request,'Product/product-list.html',context)

#admin add product
@staff_member_required(login_url='admin_login')
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST , request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Product Added success fully ')
            return redirect(product_list)
        else:
            return redirect(add_product)
    else:
        form = ProductForm()
        context = {
            'form' : form
        }
    return render(request , 'Product/add-product.html' , context)

#admin delete product
@staff_member_required(login_url='admin_login')
def product_delete(request,id):
    if request.method == 'POST' :
        category_id = Product.objects.get(pk=id)
        messages.error(request,'Product Deleted success fully ')
        category_id.delete()
    return redirect(product_list)

#admin update producr
@staff_member_required(login_url='admin_login')
def update_produect(request, id) :
    category = Product.objects.get(id=id)
    if request.method == 'POST' :
        form = ProductForm(request.POST, request.FILES, instance=category)   
        if form.is_valid() :
            form.save()
            messages.success(request,'Product Updated success fully ')
            return redirect(product_list)    
    form = ProductForm(instance=category)
    context = {'form' : form}
    return render(request, 'Product/add-product.html', context)  

@staff_member_required(login_url='admin_login')
def product_offer(request):
    product=Product.objects.all()
    paginator = Paginator(product, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context={
        'product':product,
        'page_obj':page_obj
    }
    return render(request,'Category/product-offer.html',context)

@staff_member_required(login_url='admin_login')
def add_product_offer(request):
    if request.method == 'POST' :
        product_name = request.POST.get('product_name')
        product_offer = request.POST.get('product_offer')
        product = Product.objects.get(product_name = product_name)
        product.product_offer = product_offer 
        product.save()
        messages.success(request,'Added product offer success fully')
        return redirect('product_offer')

@staff_member_required(login_url='admin_login')
def product_offer_delete(request,id):
    if request.method == 'POST' :
        product = Product.objects.get(id = id)
        product.product_offer =  0
        product.save()
        messages.success(request,'Deleted product offer successfully')
        return redirect('product_offer')