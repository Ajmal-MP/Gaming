from ast import Add
from django import forms
from .models import Order,Address,Coupon

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'phone', 'email', 'address_line_1', 'address_line_2', 'country', 'state', 'city', 'order_note']

class AdminChangeOrderStatus(forms.ModelForm):
    class Meta: 
        model=Order
        fields = ['status'] 

class DateInput(forms.DateInput):
    input_type = 'date'

class CouponForm(forms.ModelForm):
    class Meta: 
        model = Coupon      
        fields = ['code', 'discount','min_value','valid_at','active']
        widgets = {
            'valid_at': DateInput(),
        }