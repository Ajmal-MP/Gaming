from django.shortcuts import render,redirect
from .form import ProductForm
from .models import Product
from django.contrib import messages
# Create your views here.

def product_list(request):
    product=Product.objects.all()
    context={
        'product':product
    }
    return render(request,'Product/product-list.html',context)

#admin add product
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
def product_delete(request,id):
    if request.method == 'POST' :
        category_id = Product.objects.get(pk=id)
        messages.error(request,'Product Deleted success fully ')
        category_id.delete()
    return redirect(product_list)

#admin update producr
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

