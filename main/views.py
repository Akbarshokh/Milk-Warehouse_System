from . import models
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
    prod_quantity = models.ProductModel.objects.filter(is_active = True).count()
    prod_sum = 0
    for num in models.ProductLitr.objects.all():
        prod_sum += num.litr
        
    context = {
        'products' : PagenatorPage(models.ProductLitr.objects.all(), 5, request),
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
        new_product = models.ProductModel.objects.create(
            name=name
        )
        prod_litr = models.ProductLitr.objects.create(
            product_to = new_product,
            litr=litr
        )
        return redirect('dashboard_url')

def add_litr_product(request):
    if request.method == 'POST':
        litr = request.POST['litr']
        litr = float(litr)
        prod_id = request.POST['prod_id']
        product = models.ProductLitr.objects.get(id=prod_id)
        product.litr += litr
        product.save()
        return redirect('dashboard_url')
    

def substract_litr_product(request):
    if request.method == 'POST':
        litr = request.POST['litr']
        litr = float(litr)
        prod_id = request.POST['prod_id']
        product = models.ProductLitr.objects.get(id=prod_id)
        product.litr -= litr
        if product.litr < 1:
            product.is_active = False
        product.save()
        return redirect('dashboard_url')

def delete_product(request):
    if request.method == 'POST':
        prod_id =  request.POST['prod_id']
        product_litr = models.ProductLitr.objects.get(id=prod_id)
        product_litr.product_to.delete()
        product_litr.delete()
        return redirect('dashboard_url')