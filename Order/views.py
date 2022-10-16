from concurrent.futures.process import _python_exit
from multiprocessing import context
from django.shortcuts import render,redirect
from Cart.models import CartItem
from Product.models import Product
from .forms import OrderForm
from .models import Address, Order, OrderProduct, Payment,Coupon,UserCoupon
import datetime 
import json
from django.http import JsonResponse
from .forms import CouponForm
from django.core.paginator import Paginator
import razorpay
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages

# Create your views here.

client = razorpay.Client(auth=('rzp_test_N4hXBlIPwM654C', 'lFsBhsm8tCgLlSEhUX4BDH0a'))

def place_order(request,total=0,quantity=0):
    user  = request.user
    
    #if not cartitem redirect to shop

    cart_items = CartItem.objects.filter(user = user)
    cart_count =    cart_items.count()
    if cart_count <= 0:
        return redirect('store')
    
    delivery_charge = 0
    grand_total = 0
    item_total = 0
    for cart_item in cart_items:
            total += int(cart_item.product.offer_price())*int(cart_item.quantity)
            quantity += cart_item.quantity
            item_total += total 
    delivery_charge = 50 if total<=500 else 0
    grand_total = total+ delivery_charge


    if request.method == 'POST':
        id = request.POST['flexRadioDefault']
        address  = Address.objects.get(user = request.user,id = id)
        data = Order()
        data.user = request.user
        data.first_name = address.first_name
        data.last_name = address.last_name
        data.phone = address.phone
        data.email = address.email
        data.address_line_1 = address.address_line_1
        data.address_line_2 = address.address_line_2
        data.country = address.country
        data.state = address.state
        data.city = address.city
        data.order_total = grand_total
        data.delivery_charge = delivery_charge
        data.is_ordered = False
        data.ip = request.META.get('REMOTE_ADDR')
        data.save()


        #code for generating order
        yr = int(datetime.date.today().strftime('%Y'))
        dt = int(datetime.date.today().strftime('%d'))
        mt = int(datetime.date.today().strftime('%m'))
        d = datetime.date(yr,mt,dt)
        current_date = d.strftime("%Y%m%d") 
        order_number = current_date + str(data.id)
        data.order_number = order_number
        data.save()


        
        coupons = Coupon.objects.filter(active = True)

        for item in coupons:
            try:
                coupon = UserCoupon.objects.get(user = request.user,coupone = item)
            except:
                coupon = UserCoupon()
                coupon.user = request.user
                coupon.coupone = item
                coupon.order = data
                coupon.save() 


        coupons = UserCoupon.objects.filter(used = False , user = request.user)
        order = Order.objects.get(user = user, is_ordered = False, order_number = order_number)          
        context={
            'order':order,
            'cart_items':cart_items,
            'total':total,
            'grand_total':grand_total,
            'delivery_charge':delivery_charge,
            'product_order_number':order_number,
            'coupons':coupons
        }
        return render(request,'UserSide/payment.html',context)    
    else:
        return redirect('checkout')


def payments(request):
    #geting json data 
    body = json.loads(request.body)
    
    order = Order.objects.get(user = request.user, is_ordered = False, order_number = body['orderID'])
    payment = Payment(
        user = request.user,
        payment_id = body['transID'],
        order_number = order.order_number,
        payment_method = body['paymode'],
        amount_paid = order.order_total,
        status = True
    )
    payment.save()
    order.payment = payment
    order.is_ordered = True
    order.save()

    # Move cart item to orderd product table
    cart_items = CartItem.objects.filter(user = request.user)

    for cart_item in cart_items:
        order_product =  OrderProduct()
        order_product.order_id = order.id
        order_product.payment = payment
        order_product.user_id =  request.user.id
        order_product.product_id = cart_item.product_id
        order_product.quantity =  cart_item.quantity
        order_product.product_price = cart_item.product.price
        order_product.ordered = True
        order_product.save()
    #Reduce Quantity of procut
        product = Product.objects.get( id = cart_item.product_id)
        product.stock -= cart_item.quantity
        product.save()
    
    #clear cart
    CartItem.objects.filter(user = request.user).delete()
    #send order number and Transaction id to Web page using 

      
    data = {
        'order_number': order.order_number,
        'transID':payment.payment_id
        }
    return JsonResponse(data)
  



#invoice creating function
def payments_completed(request):
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')
    try:
        order = Order.objects.get(order_number = order_number)      #is_orderd = True
        ordered_products = OrderProduct.objects.filter(order_id=order.id)

        subtotal = 0
        for i in ordered_products:
            subtotal += i.product_price * i.quantity

        payment = Payment.objects.get(payment_id=transID)

        context = {
            'order': order,
            'ordered_products': ordered_products,
            'order_number': order.order_number,
            'transID': payment.payment_id,
            'payment': payment,
            'subtotal': subtotal,
        }
        return render(request, 'UserSide/payment-success.html', context)
    except (Payment.DoesNotExist, Order.DoesNotExist):
        return redirect('home')








def razor_pay(request):
        DATA = {
            "amount": 100,
            "currency": "INR",
            "receipt": "receipt#1",
            "notes": {
                "key1": "value3",
                "key2": "value2"
            }
        }
        payment = client.order.create(data=DATA)
        return JsonResponse({
            'payment':payment,
             'payment_method' : "RazorPay"
        })



def cash_on_delivery(request,id):
    # Move cart item to orderd product table
    try:
        order = Order.objects.get(user = request.user, is_ordered = False, order_number = id)
        cart_items = CartItem.objects.filter(user = request.user)
        order.is_ordered = True
        payment = Payment(
            user = request.user,
            payment_id = order.order_number,
            order_number = order.order_number,
            payment_method = 'Cash On Delivery', 
            amount_paid = order.order_total,
            status = False
        )

        payment.save()
        order.payment = payment
        order.is_ordered = True
        order.save()
        for cart_item in cart_items:
            order_product =  OrderProduct()
            order_product.order_id = order.id

            order_product.user_id =  request.user.id
            order_product.product_id = cart_item.product_id
            order_product.quantity =  cart_item.quantity
            order_product.product_price = cart_item.product.price
            order_product.ordered = True
            order_product.save()
        #Reduce Quantity of procut
            product = Product.objects.get( id = cart_item.product_id)
            product.stock -= cart_item.quantity
            product.save()

            #clear cart
            CartItem.objects.filter(user = request.user).delete()
            #send order number and Transaction id to Web page using 
            context ={
            'orders':order,
            'payment':payment
             }
            return render(request,'UserSide/cash-delivery-success.html',context)
    except:
        return redirect('home')


#order management

def user_orders(request):
    orders = Order.objects.filter(user = request.user, is_ordered = True).order_by('-created_at') 
    paginator = Paginator(orders, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'orders' : orders,
        'page_obj': page_obj
    }
    return render(request,'UserSide/dashbord/user-order-detail.html',context)


def admin_orders_list(request):
    if 'query' in request.GET:
        query = request.GET.get('query')
        print(query)
        if query:
            orders = Order.objects.filter(is_ordered = True,order_number__icontains = query).order_by('-created_at')           
        else:
            return redirect(admin_orders_list)
    else:        
        orders = Order.objects.filter(is_ordered = True).order_by('-created_at')
    paginator = Paginator(orders, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'orders' : orders,
        'page_obj': page_obj,
        'serch_item':2
    }
    return render(request,'Admin/admin-order-detail.html',context)


def update_admin_order(request,id):
    if request.method == 'POST':
        order = get_object_or_404(Order, id=id)
        status = request.POST.get('status')
        order.status = status 
        order.save()
        if status  == "Completed":
            try:
                payment = Payment.objects.get(payment_id = order.order_number, status = False)
                print(payment)
                if payment.payment_method == 'Cash On Delivery':
                    payment.status = True
                    payment.save()
            except:
                pass
        order.save()

        return redirect(admin_orders_list)


def cancel_order(request,id):
    order = Order.objects.get(order_number = id,user = request.user)
    order.status = "Cancelled"
    order.save()
    payment = Payment.objects.get(order_number = order.order_number)
    payment.delete()
    return redirect('user_orders')

def return_order(request,id):
    order = Order.objects.get(order_number = id,user = request.user)
    order.status = "Returned"
    order.save()
    payment = Payment.objects.get(payment_id = order.order_number)
    payment.delete()
    return redirect('user_orders')




def coupon(request):
    if request.method == 'POST':
        grand_total = request.POST.get('grand_total')
        coupon = request.POST.get('coupon')
        coupon_perc = 0
        try:
            instance = UserCoupon.objects.get(user = request.user ,coupone__code = coupon)
            order = Order.objects.get(user = request.user,order_coupon__coupone = instance.coupone)
            if int(grand_total) >= int(instance.coupone.min_value):
                grand_total = int(grand_total) - ((int(grand_total) * int(instance.coupone.discount))/100)
                coupon_perc = instance.coupone.discount
                msg = 'Applied coupon successfully'
                instance.used = True
                order.order_total = grand_total
                order.save()
                instance.save()
            else:
                msg='This coupon only applicable for more than '+ str(instance.coupone.min_value)+ 'rupee only!'
        except:
            msg = 'Coupon is not valid'
        response = {
                         'grand_total': grand_total,
                         'msg':msg,
                         'coupon_perc':coupon_perc
            }
        return JsonResponse(response)


def admin_display_coupon(request):
    if 'query' in request.GET:
        query = request.GET.get('query')
        print(query)
        if query:
            coupons = Coupon.objects.filter(code__icontains = query)            
        else:
            return redirect(admin_display_coupon)
    else:
        coupons = Coupon.objects.all()
    paginator = Paginator(coupons, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    print(coupons)
    context = {
        'coupons': coupons,
        'page_obj' : page_obj,
        'serch_item':8
    }
    return render(request, 'admin/admin_display_coupon.html', context)


def admin_add_coupon(request):
    if request.method == 'POST':
        form = CouponForm(request.POST , request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Coupon Added successfully')
            return redirect(admin_display_coupon)
        else:
            messages.error(request, 'Coupon with this code already exists !')
            return redirect(admin_display_coupon)
    form = CouponForm()
    today_date=str(datetime.date.today())
    context = { 
        'form':form,
        'today_date': today_date
    }
    return render(request,'Admin/admin-add-coupon.html',context)

def coupon_delete(request,id):
    if request.method == 'POST' :
        coupon = Coupon.objects.get(id=id)
        coupon.delete()
        messages.success(request, 'Coupon deleted successfully')
    return redirect(admin_display_coupon)

#admin update producr
def coupon_update(request, id) :
    category = Coupon.objects.get(id=id)
    if request.method == 'POST' :
        form = CouponForm(request.POST, request.FILES, instance=category)   
        if form.is_valid() :
            form.save()
            messages.success(request,'Coupon Updated success fully ')
            return redirect(admin_display_coupon)    
    form = CouponForm(instance=category)
    today_date=str(datetime.date.today())
    context = {'form' : form,'today_date': today_date}
    return render(request, 'Admin/admin-add-coupon.html', context)  

def invoice_download(request,id):
    try:
        if request.method == 'POST':
            order = Order.objects.get(user = request.user,id = id)
            ordered_products = OrderProduct.objects.filter(order_id=order.id)

            subtotal = 0
            for i in ordered_products:
                subtotal += i.product.sub(request) * i.quantity

            payment = Payment.objects.get(order_number=order.order_number)

            context = {
                'order': order,
                'ordered_products': ordered_products,
                'order_number': order.order_number,
                'transID': payment.payment_id,
                'payment': payment,
                'subtotal': subtotal,
            }
            return render(request, 'UserSide/invoice-download.html', context)
        else:
            return redirect('home')
    except:
        return redirect('home')