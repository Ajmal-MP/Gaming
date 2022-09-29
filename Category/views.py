from multiprocessing import context
from django.shortcuts import render,redirect
from .models import Categories,SubCategories
from .form import Categoryform, SubCategoryForm
from django.contrib.admin.views.decorators import staff_member_required 



# category views
@staff_member_required(login_url='admin_login')
def category_list(request):
    category=Categories.objects.all()
    context={
        'category':category
    }
    return render(request,'Category/category.html',context)

@staff_member_required(login_url='admin_login')
def category_add(request):
    if request.method == 'POST':
        form = Categoryform(request.POST , request.FILES)
        if form.is_valid():
            form.save()
            return redirect(category_list)
        else:
            # messages.error(request , 'Details is not valid please check it!!')
            return redirect(category_list)
    else:
        form = Categoryform()
        context = {
            'form' : form
        }
    return render(request , 'Category/category-add.html' , context)

def category_delete(request,id):
    if request.method == 'POST' :
        category_id = Categories.objects.get(pk=id)
        category_id.delete()
    return redirect(category_list)


#sub category views
@staff_member_required(login_url='admin_login')
def sub_category_list(request, id=None):
    sub_category=SubCategories.objects.filter(category = id)
    context={
        'sub_category':sub_category,
    }
    return render(request,'Category/sub-category.html',context)

@staff_member_required(login_url='admin_login')
def sub_category(request):
    sub_category=SubCategories.objects.all()
    context={
        'sub_category':sub_category,
    }
    return render(request,'Category/sub-category.html',context)



@staff_member_required(login_url='admin_login')
def sub_category_add(request):
    if request.method == 'POST':
        form = SubCategoryForm(request.POST , request.FILES)
        if form.is_valid():
            form.save()
            id = request.POST['category']
            return redirect(sub_category_list,id = id)
        else:
            # messages.error(request , 'Details is not valid please check it!!')
            return redirect(category_list)
    else:
        form = SubCategoryForm()
        context = {
            'form' : form
        }
    return render(request , 'Category/sub-category-add.html' , context)


def sub_category_delete(request,id):
    if request.method == 'POST' :
        category_id = SubCategories.objects.get(pk=id)
        category_id.delete()
    return redirect(category_list)