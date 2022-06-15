from math import prod
import re

from django.http import HttpResponse
from . models import ProductModel, MilkModel
from django.shortcuts import redirect, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def PagenatorPage(List, num, request):
    paginator = Paginator(List, num)
    pages = request.GET.get('page')

    try:
        list = paginator.page(pages)
    except PageNotAnInteger:
        list = paginator.page(1)
    except EmptyPage:
        list = paginator.page(paginator.num_pages)
    return list


def dashboard(request):    
    prod_quantity = ProductModel.objects.filter(is_active = True).count()
    milk_litr = MilkModel.objects.first().litr

    try:
        prod_sum = 0
        for num in ProductModel.objects.all():
            prod_sum += num.litr
    except:
        prod_quantity = 0
    search = request.GET.get('q')
    if search != '' and search is not None:
        products = ProductModel.objects.filter(name__icontains=search).filter(is_active=True)
    else:
        products = ProductModel.objects.filter(is_active = True)
    context = {
        'products' : PagenatorPage(products, 5, request),
        'prod_sum':prod_sum,
        'prod_quantity':prod_quantity,
        'milk_litr':milk_litr
    }
    return render(request, 'dashboard.html', context)

def login_view(request):
    return render(request, 'login.html')


def logout_view(request):
    return render(request, 'logout.html')

def add_product(request):
    if request.method == 'POST':
        name = request.POST['name']
        ProductModel.objects.create(
            name=name,
        )
        return redirect('dashboard_url')

def add_litr_product(request):
    if request.method == 'POST':
        litr = request.POST['litr']
        litr = float(litr)
        prod_id = request.POST['prod_id']
        product = ProductModel.objects.get(id=prod_id)
        product.litr += litr
        product.save()
        return redirect('dashboard_url')
    

def substract_litr_product(request):
    if request.method == 'POST':
        litr = request.POST['litr']
        litr = float(litr)
        prod_id = request.POST['prod_id']
        product = ProductModel.objects.get(id=prod_id)
        product.litr -= litr
        if product.litr < 1:
            product.is_active = False
        product.save()
        return redirect('dashboard_url')

def delete_product(request):
    if request.method == 'POST':
        prod_id =  request.POST['prod_id']
        product_litr = ProductModel.objects.get(id=prod_id)
        product_litr.delete()
        return redirect('dashboard_url')

def make_product(request):
    products = ProductModel.objects.filter(is_active = True)
    milk = MilkModel.objects.first()
    if request.method == 'POST':
        product_id = request.POST['product']
        quantity = request.POST['quantity']
        quantity = float(quantity)
        if quantity > milk.litr:
            return HttpResponse('sut yetarlik emas')
        else:
            product = ProductModel.objects.get(id=product_id)
            product.litr += quantity
            product.save()
            milk.litr -=quantity
            milk.save()
        return redirect('dashboard_url')
    context = {
        'products':products
    }
    return render(request, 'new_products.html', context)

def add_milk(request):
    if request.method == 'POST':
        litr = request.POST['litr']
        try:
            milk = MilkModel.objects.first()
            print(milk.litr)
            milk.litr += float(litr)
        except:
            milk = MilkModel.objects.create(
                litr=litr
            )
        milk.save()
        return redirect('dashboard_url')