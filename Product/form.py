from .models import Product
from django import forms
class ProductForm(forms.ModelForm):
    class Meta:
        model=Product     
        fields= ['product_name','slug','brand','price','product_image_1','product_image_2','product_image_3','product_image_4','product_description','category_id','subcategory_id','stock','is_active']
        


        