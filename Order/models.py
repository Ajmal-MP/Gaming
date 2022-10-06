from itertools import product
from operator import mod
from django.db import models
from Accounts.models import Account
from Product.models import Product
from django.core.validators import MinValueValidator,MaxValueValidator
# Create your models here.

class Payment(models.Model):
    user           = models.ForeignKey(Account, on_delete=models.CASCADE)
    payment_id     = models.CharField(max_length=100)
    order_number   =models.IntegerField()
    payment_method = models.CharField(max_length=100)
    amount_paid    = models.CharField(max_length=100)
    status         = models.BooleanField()
    created_at     = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payment_id  

class Order(models.Model):
    STATUS = (
        ('Order Conformed', 'Order Confirmed'),
        ('Shipped',"Shipped"),
        ('Out for delivery',"Out for delivery"),
        ('Completed', 'Completed'),
        ('Cancelled','Cancelled')
    )
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True,related_name='order_payment')
    order_number = models.CharField(max_length=20)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=50)
    address_line_1 = models.CharField(max_length=50)
    address_line_2 = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    order_note = models.CharField(max_length=100, blank=True)
    order_total = models.FloatField()
    delivery_charge = models.FloatField()
    status = models.CharField(max_length=50, choices=STATUS, default='Order Confirmed')
    ip = models.CharField(blank=True, max_length=20)
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.payment)
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def full_address(self):
        return f'{self.address_line_1} {self.address_line_2}'    

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='user_order_page')
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    product_price = models.FloatField()
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.product.product_name


class Address(models.Model):
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=50)
    address_line_1 = models.CharField(max_length=50)
    address_line_2 = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)

    def full_name(self):
        return f'{self.first_name} {self.last_name}'


class Coupon(models.Model):
    code = models.CharField(max_length=50,unique=True)
    discount = models.IntegerField(validators = [MinValueValidator(0),MaxValueValidator(20)])
    min_value = models.IntegerField(validators = [MinValueValidator(0)])
    valid_from = models.DateTimeField(auto_now_add=True)
    valid_at = models.DateField()
    active = models.BooleanField(default=False)
    def __str__(self):
        return self.code

class UserCoupon(models.Model):
    user =  models.ForeignKey(Account,on_delete=models.CASCADE, null= True)
    coupone = models.ForeignKey(Coupon,on_delete = models.CASCADE, null = True)
    order  = models.ForeignKey(Order,on_delete=models.SET_NULL,null = True,related_name='order_coupon')
    used = models.BooleanField(default = False)
    def __str__(self):  
        return str(self.id)