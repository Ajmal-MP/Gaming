from django.shortcuts import render
from Product.models import Product
def home(request):
    product = Product.objects.filter(is_active = True)
    context = {
        'products': product
    }
    return render(request, 'Accounts/home.html',context)