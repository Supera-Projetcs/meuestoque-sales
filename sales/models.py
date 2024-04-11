from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Product(models.Model):
    id_produto = models.IntegerField()
    unit_value = models.FloatField()
    quantity = models.IntegerField()


class Sale(models.Model):
    produtos = models.ManyToManyField(Product, related_name="products_sales")
    date_sold = models.DateTimeField(auto_now_add=True)
