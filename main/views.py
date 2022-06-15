from math import prod

from django.http import HttpResponse
from . models import ProductModel
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
    prod_sum = 0
    for num in ProductModel.objects.all():
        prod_sum += num.litr
    search = request.GET.get('q')
    if search != '' and search is not None:
        products = ProductModel.objects.filter(name__icontains=search).filter(is_active=True)
    else:
        products = ProductModel.objects.filter(is_active = True)
    context = {
        'products' : PagenatorPage(products, 5, request),
        'prod_sum':prod_sum,
        'prod_quantity':prod_quantity
    }
    return render(request, 'dashboard.html', context)

def login_view(request):
    return render(request, 'login.html')


def logout_view(request):
    return render(request, 'logout.html')

def add_product(request):
    if request.method == 'POST':
        name = request.POST['name']
        litr = request.POST['litr']
        ProductModel.objects.create(
            name=name,
            litr = litr
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
    if request.method == 'POST':
        name = request.POST['name']
        product_id = request.POST['product']
        quantity = request.POST['quantity']
        quantity = float(quantity)
        product = ProductModel.objects.get(id=product_id)
        product.litr -= quantity
        if product.litr <0:
            # shu yerga message return qilishi kerak, test uchun http response qilib qo`ydim
            return HttpResponse('maxsulot hajmi yetarlik emas')
        elif product.litr == 0:
            product.is_active = False
            product.save()
        else:
            product.save()
            ProductModel.objects.create(
                name=name,
                litr=quantity
            )
    context = {
        'products':products
    }
    return render(request, 'new_products.html', context)