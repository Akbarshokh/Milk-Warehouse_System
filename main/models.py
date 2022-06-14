from audioop import maxpp
from turtle import rt
from django.db import models


class ProductModel(models.Model):
    name = models.CharField(max_length=250)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
class ProductLitr(models.Model):
    product_to = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    litr = models.FloatField()
    
    def __str__(self):
        return self.product_to.name