from django.db.models import Sum
from decimal import Decimal
from django.db.models import F




from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Sale
from .serializers import SaleSerializer
import requests

@api_view(['GET', 'POST'])
def sale_list(request):
    if request.method == 'GET':
        sales = Sale.objects.all()
        serializer = SaleSerializer(sales, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        sale_serializer = SaleSerializer(data=request.data)
        if sale_serializer.is_valid():
            product_id = request.data.get('inventory_id')
            quantity = request.data.get('quantity')

            product_url = f"http://inventorys/id/{product_id}"
            try:
                response = requests.get(product_url)
                response.raise_for_status()  

                product_data = response.json()

                sale_data = {
                    'product_name': product_data.get('product_name'),
                    'quantity': quantity,
                    'price': product_data.get('price'),
                }

                sale_serializer = SaleSerializer(data=sale_data)
                if sale_serializer.is_valid():
                    sale_serializer.save()
                    return Response(sale_serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(sale_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except requests.exceptions.RequestException as e:
                return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(sale_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def sales_report(request):
    total_sales_count = Sale.objects.count()  

    product_info_url = "http://url-do-outro-servico/product/info"
    try:
        response = requests.get(product_info_url)
        response.raise_for_status()  
        product_info = response.json()
        product_price = Decimal(product_info.get('price'))
        best_selling_product_name = product_info.get('best_selling_product_name')
    except requests.exceptions.RequestException as e:
        return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    total_sales_price = Decimal(0)
    for sale in Sale.objects.all():
        total_sales_price += sale.quantity * product_price

    return Response({
        'total_sales_count': total_sales_count,
        'total_sales_price': round(total_sales_price, 2),
        'best_selling_product_name': best_selling_product_name,
    })