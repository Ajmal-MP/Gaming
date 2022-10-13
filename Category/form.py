from django import forms
from .models import Categories,SubCategories
class Categoryform(forms.ModelForm):

    class Meta:
        model = Categories
        fields = ['category_name' ,'slug']  

class SubCategoryForm(forms.ModelForm):

    class Meta:
        model = SubCategories
        fields = ['sub_category_name', 'slug', 'category']
