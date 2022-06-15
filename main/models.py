from django.db import models

class MilkModel(models.Model):
    litr = models.FloatField()

    def __str__(self):
        return str(self.litr)

class ProductModel(models.Model):
    name = models.CharField(max_length=250)
    is_active = models.BooleanField(default=True)
    litr = models.FloatField(default=0)

    def __str__(self):
        return self.name
    