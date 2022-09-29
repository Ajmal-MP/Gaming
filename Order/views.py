from concurrent.futures.process import _python_exit
from django.shortcuts import render,redirect
from Cart.models import CartItem
from Product.models import Product
from .forms import OrderForm
from .models import Address, Order, OrderProduct, Payment
import datetime 
import json
from django.http import JsonResponse
from .forms import AdminChangeOrderStatus
from django.core.paginator import Paginator
import razorpay
from django.shortcuts import get_object_or_404
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
        form = OrderForm(request.POST)

        if form.is_valid():
            # store  the billing informations
            data = Order()
            #address detail 
            detail = Address()
            detail.user = data.user = request.user
            detail.first_name = data.first_name = form.cleaned_data['first_name']
            detail.last_name = data.last_name = form.cleaned_data['last_name']
            detail.phone = data.phone = form.cleaned_data['phone']
            detail.email = data.email = form.cleaned_data['email']
            detail.address_line_1 = data.address_line_1 = form.cleaned_data['address_line_1']
            detail.address_line_2 = data.address_line_2 = form.cleaned_data['address_line_2']
            detail.country = data.country = form.cleaned_data['country']
            detail.state = data.state = form.cleaned_data['state']
            detail.city = data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.delivery_charge = delivery_charge
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            try:
                ans =Address.objects.filter(user = request.user,
                 last_name = detail.last_name,
                 first_name=detail.first_name,
                 phone = detail.phone,
                 email = detail.email,
                 address_line_1=detail.address_line_1,
                 address_line_2=detail.address_line_2,
                 country=detail.country,
                 state=detail.state,
                 city=detail.city,
                 ).exist()
                print(ans)
            except:
                pass
            # detail.save()


            #code for generating order
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d") 
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            order = Order.objects.get(user = user, is_ordered = False, order_number = order_number)          
            context={
                'order':order,
                'cart_items':cart_items,
                'total':total,
                'grand_total':grand_total,
                'delivery_charge':delivery_charge,
                'product_order_number':order_number
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
            payment_method = 'Cash On Delivery', 
            amount_paid = order.order_total,
            status = False
        )
        payment.save()
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
            'orders':order
             }
            return render(request,'UserSide/cash-delivery-success.html',context)
    except:
        return redirect('home')


#order management

def user_orders(requst):
    orders = Order.objects.filter(user = requst.user, is_ordered = True)
    context = {
        'orders' : orders
    }
    return render(requst,'UserSide/dashbord/user-order-detail.html',context)


def admin_orders_list(request):
    orders = Order.objects.all().order_by('-created_at')
    paginator = Paginator(orders, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'orders' : orders,
        'page_obj': page_obj
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
    payment = Payment.objects.get(payment_id = order.order_number)
    payment.delete()
    return redirect('user_orders')

def return_order(request,id):
    order = Order.objects.get(order_number = id,user = request.user)
    order.status = "Returned"
    order.save()
    payment = Payment.objects.get(payment_id = order.order_number)
    payment.delete()
    return redirect('user_orders')