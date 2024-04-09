from django.db import models

class Sale(models.Model):
    quantity = models.IntegerField()
    date_sold = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} units"