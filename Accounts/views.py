
from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404

from Cart.models import Cart, CartItem
from Cart.views import _cart_id, add_cart
from .models import Account
from django.contrib import messages,auth
from .verify import send_otp, verify_otp
from .form import *
from .models import *
from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required
from .form import RegistrtationForm,UserUpdationForm
from Order.models import Address
from django.core.paginator import Paginator

# Create your views here.
def Register(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method=='POST':
        form=RegistrtationForm(request.POST)
        if form.is_valid():
            first_name = request.POST['first_name']
            last_name  = request.POST['last_name']
            email      = request.POST['email']
            mobile     = request.POST['mobile']
            password   = request.POST['password']

            request.session['first_name'] = first_name
            request.session['last_name']  = last_name
            request.session['email']      = email
            request.session['mobile']     = mobile
            request.session['password']   = password
            send_otp(mobile)
            return redirect('verify')
        else:
            messages.error(request,'User with email or mobile already exists !')
            return redirect(Register)
    form=RegistrtationForm()
    context ={'form':form}
    return render(request,'Accounts/register.html',context)

def Login(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            person = Account.objects.get(email=email)
        except :
            messages.error(request,"User Does not exist..")
            return redirect(Login)

        user = authenticate(request,email=email,password=password)
              
        if user is not None:
            if person.is_active:
                try:
                    cart = Cart.objects.get(cart_id = _cart_id(request))
                    is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                    
                    if is_cart_item_exists:
                        cart_item = CartItem.objects.filter(cart=cart)
                        for item in cart_item:
                            try:
                                cart_item = CartItem.objects.get(product=item.product,user=user)
                                cart_item.quantity += 1

                            except CartItem.DoesNotExist:
                                cart_item = CartItem.objects.create(
                                    product = item.product,
                                    quantity = 1,
                                    user=user
                                    )
                            cart_item.save()
                except:
                    pass
                auth.login(request,user)
                return redirect('home')
            elif person.is_active == False:
                messages.error(request,"Account is Blocked..")
        else:
            messages.error(request,'Invalid Password')
            return redirect('login')
    return render(request,'Accounts/login.html')


def Logout(request):
    logout(request)
    return redirect('home')



def verify_code(request):
    if  request.method == 'POST':
        otp_check = request.POST.get('otp')
        mobile=request.session['mobile']

        verify=verify_otp(mobile,otp_check)

        if  verify:
            first_name = request.session['first_name']
            last_name  = request.session['last_name']
            email      = request.session['email']
            mobile     = request.session['mobile']
            password   = request.session['password']

            user = Account.objects.create_user(
                first_name =  first_name,
                last_name  =  last_name,
                email      =  email,
                mobile     =  mobile,
                password   =  password
            )
            user.is_verified = True
            user.save()
            messages.success(request,'Registration Successful login now !')
            return redirect('login')
        
        else:
            messages.error(request,'invalid otp recheck')
            return redirect (verify_code)
        
    return render(request,'Accounts/verify.html')




#user details


def user_dashbord(request):
    return render(request,'UserSide/dashbord/user-dashbord.html')

def account_detail(request):
    user_details=Account.objects.filter(id = request.user.id)
    context={
        'user_detail':user_details
    }
    return render(request,'UserSide/dashbord/account-detail.html',context)

def account_detail_update(request):
    id=Account.objects.get(id = request.user.id)
    if request.method == 'POST':
        form = UserUpdationForm(request.POST , request.FILES, instance=id)
        if form.is_valid():
            form.save()
            messages.error(request , 'Updated Successfully')
            return redirect(account_detail)
        else:
            messages.error(request , 'Details is not valid please check it!!')
            return redirect(account_detail)
    else:
        form = UserUpdationForm(instance=id)
        context = {
            'form' : form,
        }
    return render(request , 'UserSide/dashbord/account-detail-update.html' , context)



# Address manage ment
def addresses(request):
    addresses=Address.objects.filter(user = request.user)
    paginator = Paginator(addresses, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context={
        'addresses':addresses,
        'page_obj':page_obj
    }
    return render(request,'UserSide/dashbord/address.html',context)


#user add address
def add_address(request):
    if request.method == 'POST':
        form = AddAddress(request.POST,request.FILES,)
        if form.is_valid():
            print('form is valid')
            detail = Address()
            detail.user = request.user
            detail.first_name =form.cleaned_data['first_name']
            detail.last_name = form.cleaned_data['last_name']
            detail.phone =  form.cleaned_data['phone']
            detail.email =  form.cleaned_data['email']
            detail.address_line_1 =  form.cleaned_data['address_line_1']
            detail.address_line_2  = form.cleaned_data['address_line_2']
            detail.country =  form.cleaned_data['country']
            detail.state =  form.cleaned_data['state']
            detail.city =  form.cleaned_data['city']
            detail.save()
            messages.success(request,'Address is Added Successfully')
            return redirect(addresses)
        else:
            messages.success(request,'Form is Not valid')
            return redirect(addresses)
    else:
        form = AddAddress()
        context={
            'form':form
        }    
    return render(request,'UserSide/dashbord/user-add-address.html',context)

#address update
def update_address(request,id):
    id=Address.objects.get(id = id)
    if request.method == 'POST':
        form = AddAddress(request.POST, instance=id)
        if form.is_valid():
            form.save()
            messages.error(request , 'Updated Successfully')
            return redirect(addresses)
        else:
            messages.error(request , 'Details is not valid please check it!!')
            return redirect(addresses)
    else:
        form = AddAddress(instance=id)
        context = {
            'form' : form,
        }
    return render(request , 'UserSide/dashbord/user-address-update.html' , context)



def delete_address(request,id):
    address=Address.objects.get(id = id)
    messages.success(request,"Address Deleted")
    address.delete()
    return redirect(addresses)

