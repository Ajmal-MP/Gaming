from django.contrib import messages
from django.shortcuts import render,redirect
from django.contrib.auth import logout,login,authenticate
from .form import UserForm,Account
from django.contrib.admin.views.decorators import staff_member_required  
from Order.models import Order, Payment
from datetime import datetime,timedelta
from django.db.models import Sum
from Product.models import Product
# Create your views here.
def Admin_login(request):
    
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request,email=email,password=password)
        if user is not None:
            login(request,user)
            return redirect(dashbord) 
        else:
            messages.error(request,'user does not exist..')
            return redirect(Admin_login)
    return render(request,'Admin/login.html')



@staff_member_required(login_url='admin_login')
def Admin_logout(request):
    logout(request)
    return redirect(Admin_login)



#To display all user
@staff_member_required(login_url='admin_login')
def user_display(request):
    user=Account.objects.filter(is_superadmin = False)
    form = UserForm()
    context={
        'user':user,
        'form':form
    }
    return render(request,'Admin/admin-display-user.html',context) 

@staff_member_required(login_url='admin_login')
def user_block(request,id,flag):
    if request.method == 'POST':
         person = Account.objects.get( id = id)
         if flag ==1:
            person.is_active = False
            person.save()
         else: 
            person.is_active = True
            person.save()
         return redirect(user_display)

@staff_member_required(login_url='admin_login')
def sales_report(request):
    today = datetime.today()
    month = today.month
    orders = Order.objects.filter(created_at__month=month,payment__status = True).values('user_order_page__product__product_name','user_order_page__product__stock',total = Sum('order_total'),).annotate(dcount=Sum('user_order_page__quantity')).order_by()
    total_payment_amount = Payment.objects.filter(status = True,created_at__month=month).aggregate(Sum('amount_paid'))
    print(total_payment_amount)
    context = {
        'orders':orders,
        'total_payment_amount':total_payment_amount,
    }
    return render(request,'Admin/sales-report.html',context)  

@staff_member_required(login_url='admin_login')
def year_sales_report(request):
    year = datetime.now().year
    print(year)
    orders = Order.objects.filter(created_at__year=year,payment__status = True).values('user_order_page__product__product_name','user_order_page__product__stock',total = Sum('order_total'),).annotate(dcount=Sum('user_order_page__quantity')).order_by()
    total_payment_amount = Payment.objects.filter(status = True,created_at__year=year).aggregate(Sum('amount_paid'))
    context = {
        'orders':orders,
        'total_payment_amount':total_payment_amount,
    }
    return render(request,'Admin/sales-report.html',context) 





@staff_member_required(login_url='admin_login')
def dashbord(request):
    today = datetime.today()
    month = today.month
    month = today.month
    day = today.day
    one_week = datetime.today() - timedelta(days=7)
    order_count_in_month = Order.objects.filter(created_at__month=month).count()
    order_count_in_day =Order.objects.filter(created_at__day = day).count()
    order_count_in_week = Order.objects.filter(created_at__gte = one_week).count()
    number_of_users  = Account.objects.filter(is_admin = False).count()
    paypal_orders = Payment.objects.filter(payment_method="PayPal",status = True).count()
    razorpay_orders = Payment.objects.filter(payment_method="RazerPay",status = True).count()
    cash_on_delivery_count = Payment.objects.filter(payment_method="Cash On Delivery",status = True).count()

    total_payment_count = paypal_orders + razorpay_orders +cash_on_delivery_count
    total_payment_amount = Payment.objects.filter(status = True).aggregate(Sum('amount_paid'))


    #status
    orderd = Order.objects.filter(status = 'Order Confirmed').count()
    shipped = Order.objects.filter(status = "Shipped").count()
    out_of_delivery = Order.objects.filter(status ="Out for delivery").count()
    completed = Order.objects.filter(status = "Completed").count()


    context ={
        'order_count_in_month':order_count_in_month,
        'order_count_in_day':order_count_in_day,
        'order_count_in_week':order_count_in_week,
        'number_of_users':number_of_users,
        'paypal_orders':paypal_orders,
        'razorpay_orders':razorpay_orders,
        'total_payment_count':total_payment_count,
        'total_payment_amount':total_payment_amount,
        'orderd':orderd,
        'shipped':shipped,
        'out_of_delivery':out_of_delivery,
        'completed':completed,
        'cash_on_delivery_count':cash_on_delivery_count
        
    }
    return render(request,'Admin/dashbord.html',context)