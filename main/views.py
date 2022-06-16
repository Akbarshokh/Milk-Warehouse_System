from django.http import HttpResponse
from . models import ProductModel, MilkModel
from django.shortcuts import redirect, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

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

@login_required(login_url='login_url')
def dashboard(request):    
    prod_quantity = ProductModel.objects.filter(is_active = True).count()
    try:
        milk_litr = MilkModel.objects.first().litr
    except:
        milk_litr = MilkModel.objects.create(
            litr = 0
        )
  
    table_products = ProductModel.objects.filter(is_active = True)[:4]
    products = ProductModel.objects.all()
    context = {
        'products' : products,
        'prod_quantity':prod_quantity,
        'milk_litr':milk_litr,
        'table_products':table_products
    }
    return render(request, 'dashboard.html', context)

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('dashboard_url')
            else:
                return HttpResponse('Disabled account')
        else:
            return HttpResponse('Invalid login')
    return render(request, 'login.html')


def logout_view(request):
        logout(request)
        return redirect("login_url")

@login_required(login_url='login_url')
def add_product(request):
    if request.method == 'POST':
        name = request.POST['name']
        ProductModel.objects.create(
            name=name,
        )
        return redirect('dashboard_url')

@login_required(login_url='login_url')
def add_litr_product(request):
    if request.method == 'POST':
        litr = request.POST['litr']
        litr = float(litr)
        prod_id = request.POST['prod_id']
        product = ProductModel.objects.get(id=prod_id)
        product.litr += litr
        product.save()
        return redirect('dashboard_url')
    

@login_required(login_url='login_url')
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

@login_required(login_url='login_url')
def delete_product(request):
    if request.method == 'POST':
        prod_id =  request.POST['prod_id']
        product_litr = ProductModel.objects.get(id=prod_id)
        product_litr.delete()
        return redirect('dashboard_url')

@login_required(login_url='login_url')
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

@login_required(login_url='login_url')
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

@login_required(login_url='login_url')
def products_list(request):
    search = request.GET.get('q')
    if search != '' and search is not None:
        products = ProductModel.objects.filter(name__icontains=search)
    else:
        products = ProductModel.objects.all()
    return render(request, 'products.html', {'products':PagenatorPage(products,10, request)})