from itertools import product
from django.shortcuts import render,redirect,get_object_or_404
from Product.models import Product
from .models import  Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from Accounts.form import AddAddress
from Order.models import Address
from Accounts.models import Account
# Create your views here.


def cart(request, total=0, quantity=0, cart_items=None):
    delivery_charge = 0
    grand_total = 0
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user = request.user, is_active=True)
        else:
            cart = Cart.objects.get( cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
            
        for cart_item in cart_items:
            total += int(cart_item.product.offer_price())*int(cart_item.quantity)
            quantity += cart_item.quantity
        delivery_charge = 50 if total<=500 else 0
        grand_total = total + delivery_charge
    except ObjectDoesNotExist:
        pass


    context={
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'delivery_charge':delivery_charge,
        'grand_total' : grand_total
    }

    return render(request,'UserSide/cart.html',context)


def add_cart(request,product_id):

        user = request.user
        product = Product.objects.get(id = product_id)


        if user.is_authenticated:
            
            is_cart_item_exists = CartItem.objects.filter(product = product , user = user).exists()

            if is_cart_item_exists:
                cart_item = CartItem.objects.get(product = product , user = user)
                cart_item.quantity += 1
                cart_item.save()
            else:
                cart_item = CartItem.objects.create(
                    product = product,
                    quantity = 1,#for new cart quantity == 1
                    user = user
                )
                cart_item.save()
                
        else:
            try:
                cart = Cart.objects.get(cart_id = _cart_id(request) ) # to get cart usign cart_id session
            except Cart.DoesNotExist:
                cart = Cart.objects.create(
                    cart_id = _cart_id(request)
                   
                )
                print(cart.cart_id)
            cart.save()

            

            try:
                cart_item = CartItem.objects.get(product = product, cart = cart)
                cart_item.quantity += 1 # To increment quantity by one when click add cart
                cart_item.save()
            except CartItem.DoesNotExist:
                cart_item = CartItem.objects.create(
                    product = product,
                    quantity = 1,#for new cart quantity == 1
                    cart = cart
                )
                cart_item.save()
            
        return redirect('cart')

# to decrement cart items quantity
def remove_cart(request,product_id):
    product = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated: 
            cart_item = CartItem.objects.get(product=product, user=request.user)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart)

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')

#to remove cart items

def remove_cart_items(request,product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:   
        cart_item = CartItem.objects.get(product=product, user=request.user)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect('cart')





# To get cart_id
def _cart_id(request):
    cart = request.session.session_key

    if not cart:
        cart = request.session.create()
    return cart


@login_required(login_url='login')
def checkout(request,total=0, quantity=0, cart_items=None):
    try:
        address=Address.objects.filter(user = request.user)[:1].get()
    except:
        address = Address()
        user_detail=Account.objects.get(id = request.user.id)
        address.first_name = user_detail.first_name
        address.last_name = user_detail.last_name
        address.phone = user_detail.mobile
        address.email = user_detail.email
        address.save()



    addresses = Address.objects.filter(user  = request.user)
    try:
        if request.user.is_authenticated:   
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
       
        for cart_item in cart_items:
            total += int(cart_item.product.offer_price())*int(cart_item.quantity)
            quantity += cart_item.quantity
        delivery_charge = 50 if total<=500 else 0
        grand_total = total+ delivery_charge

    except ObjectDoesNotExist:
        pass

    context = { 
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items, 
        'detail':address,
        'addresses':addresses,
        'delivery_charge':delivery_charge,
        'grand_total' : grand_total
    }
    return render(request,'UserSide/checkout.html',context)

def checkout_address(request,id):
    address = Address.objects.get(id=id)
    print(address.first_name)
    context={
        'detail':address,
    }
    return render(request,'UserSide/dashbord/checkout-address.html',context)