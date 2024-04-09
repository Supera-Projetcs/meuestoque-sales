# from django.db.models.signals import post_save
# from django.dispatch import receiver
# import requests
# from .models import Sale

# @receiver(post_save, sender=Sale)
# def update_inventory(sender, instance, created, **kwargs):
#     if created:  
#         sale_data = {
#             'id': instance.product.id,
#             'quantity': instance.quantity,
#         }
#         try:
#             response = requests.put('http://localhost:3001/inventorys/update-quantities', json=sale_data)
#             response.raise_for_status()
#             print("Inventory quantities updated successfully")
#         except requests.exceptions.RequestException as e:
#             print(f"Error updating inventory quantities: {str(e)}")
