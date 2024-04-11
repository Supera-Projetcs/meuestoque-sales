from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Product
from .requests import inventory_update_quantity


@receiver(post_save, sender=Product)
def update_inventory(sender, instance, created, **kwargs):
    if created:
        inventory_update_quantity(instance.id_produto, instance.quantity)
