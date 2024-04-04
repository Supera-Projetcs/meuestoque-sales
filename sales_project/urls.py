
from django.contrib import admin
from django.urls import path
from sales.views import sale_list, sales_report

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sales/', sale_list),
    path('sales-report/', sales_report),

]
