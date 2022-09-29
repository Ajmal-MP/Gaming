from django.db import models
from django.urls import reverse
# Create your models here.

class Categories(models.Model):
    id =  models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=255)
    category_offer = models.IntegerField(null = True)
    slug = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
    


    def __str__(self):
        return self.category_name

    

class SubCategories(models.Model):
    sub_category_name =models.CharField(max_length=225,db_index=True)
    category         =models.ForeignKey(Categories,on_delete=models.CASCADE,related_name='category')
    slug             =models.SlugField(max_length=225,unique=True)
    is_active        =models.BooleanField(default=True)

    class Meta:
        verbose_name = 'SubCategory'
        verbose_name_plural = 'SubCategories'
    def __str__(self):
        return self.sub_category_name 

