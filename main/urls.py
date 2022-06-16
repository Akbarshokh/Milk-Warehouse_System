from django.urls import path
from .views import *

urlpatterns = [
    path('', dashboard, name='dashboard_url'),
    path('login/', login_view, name='login_url'),
    path('logout/', logout_view, name='logout_url'),
    path('add/product/', add_product, name='add_product_url'),
    path('substract/product/', substract_litr_product, name='substract_product_url'),
    path('delete/product/', delete_product, name='delete_product_url'),
    path('update/product/', add_litr_product, name='update_product_url'),
    path('make/product/', make_product, name='make_product_url'),
    path('add/litr/', add_milk, name='add_milk_url'),
    path('products/', products_list, name='products_url')
]