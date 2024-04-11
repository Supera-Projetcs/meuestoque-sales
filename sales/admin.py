from django.contrib import admin
from .models import Sale, Product


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    pass


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass
