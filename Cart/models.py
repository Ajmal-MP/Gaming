from django.db import models
from Accounts.models import Account
from Product.models import Product
# Create your models here.

class Cart(models.Model):
    cart_id = models.CharField(max_length = 250, blank = True)
    date_added = models.DateTimeField(auto_now_add = True )
    

class CartItem(models.Model):
    product =  models.ForeignKey(Product, on_delete = models.CASCADE)
    user =  models.ForeignKey(Account,on_delete=models.CASCADE, null= True)
    cart = models.ForeignKey(Cart, on_delete = models.CASCADE, null= True,related_name='cart')
    quantity = models.IntegerField()
    is_active = models.BooleanField(default = True)

    def __str__(self):
            return str(self.product)

    def sub_total(self):
        return int(self.product.offer_price())*int(self.quantity)