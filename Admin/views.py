from django.contrib import messages
from django.shortcuts import render,redirect
from django.contrib.auth import logout,login,authenticate
from requests import delete
from .form import UserForm,Account
from django.contrib.admin.views.decorators import staff_member_required  
from Order.models import Order, Payment
from datetime import datetime,timedelta
from django.db.models import Sum,Q
from django.core.paginator import Paginator
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
    paginator = Paginator(user, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    form = UserForm()
    context={
        'user':user,
        'form':form,
        'page_obj': page_obj
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
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        val = datetime.strptime(end_date, '%Y-%m-%d')
        end_date = val+timedelta(days=1)
        orders = Order.objects.filter(Q(created_at__lt=end_date),Q(created_at__gte=start_date),payment__status = True).values('user_order_page__product__product_name','user_order_page__product__stock',total = Sum('order_total'),).annotate(dcount=Sum('user_order_page__quantity')).order_by()
    else:
        today = datetime.today()
        year = datetime.now().year
        month = today.month
        orders = Order.objects.filter(created_at__year = year,created_at__month=month,payment__status = True).values('user_order_page__product__product_name','user_order_page__product__stock',total = Sum('order_total'),).annotate(dcount=Sum('user_order_page__quantity')).order_by()
    context = {
        'orders':orders,
    }
    return render(request,'Admin/sales-report.html',context)  

@staff_member_required(login_url='admin_login')
def year_sales_report(request):
    year = datetime.now().year
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
    today_date = today.strftime("%Y-%m-%d")
    month = today.month
    year = today.strftime("%Y")
    one_week = datetime.today() - timedelta(days=7)
    order_count_in_month = Order.objects.filter(created_at__year = year,created_at__month=month).count() 
    order_count_in_day =Order.objects.filter(created_at__date = today).count()
    order_count_in_week = Order.objects.filter(created_at__gte = one_week).count()
    number_of_users  = Account.objects.filter(is_admin = False).count()
    paypal_orders = Payment.objects.filter(payment_method="PayPal",status = True).count()
    razorpay_orders = Payment.objects.filter(payment_method="RazerPay",status = True).count()
    cash_on_delivery_count = Payment.objects.filter(payment_method="Cash On Delivery",status = True).count()

    total_payment_count = paypal_orders + razorpay_orders +cash_on_delivery_count
    total_payment_amount = Payment.objects.filter(status = True).aggregate(Sum('amount_paid'))

    blocked_user = Account.objects.filter(is_active = False,is_superadmin = False).count()
    unblockd_user = Account.objects.filter(is_active = True,is_superadmin = False).count()

    today_sale = Order.objects.filter(created_at__date = today_date,payment__status = True).count()
    today = today.strftime("%A")
    new_date = datetime.today() - timedelta(days = 1)
    yester_day_sale =   Order.objects.filter(created_at__date = new_date,payment__status = True).count()  
    yesterday = new_date.strftime("%A")
    new_date = new_date - timedelta(days = 1)
    day_2 = Order.objects.filter(created_at__date = new_date,payment__status = True).count()
    day_2_name = new_date.strftime("%A")
    new_date = new_date - timedelta(days = 1)
    day_3 = Order.objects.filter(created_at__date = new_date,payment__status = True).count()
    day_3_name = new_date.strftime("%A")
    new_date = new_date - timedelta(days = 1)
    day_4 = Order.objects.filter(created_at__date = new_date,payment__status = True).count()
    day_4_name = new_date.strftime("%A")
    new_date = new_date - timedelta(days = 1)
    day_5 = Order.objects.filter(created_at__date = new_date,payment__status = True).count()
    day_5_name = new_date.strftime("%A")
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
        'cash_on_delivery_count':cash_on_delivery_count,
        'blocked_user':blocked_user,
        'unblockd_user':unblockd_user,
        'today_sale':today_sale,
        'yester_day_sale':yester_day_sale,
        'day_2':day_2,
        'today':today,
        'yesterday':yesterday,
        'day_2_name':day_2_name,
        'day_3_name':day_3_name,
        'day_4_name':day_4_name,
        'day_5_name':day_5_name
        
    }
    return render(request,'Admin/dashbord.html',context)