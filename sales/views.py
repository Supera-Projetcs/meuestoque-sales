from decimal import Decimal
from django.http import JsonResponse
from collections import defaultdict

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
        sale_serializer = SaleSerializer(data=request.data, many=True)  
        if sale_serializer.is_valid():
            products_data = request.data  
            sales_data = []
            product_ids = ','.join([str(product_data['id']) for product_data in products_data])  

            product_url = f"http://localhost:3001/inventorys/by-ids/?ids={product_ids}"
            try:
                response = requests.get(product_url)
                response.raise_for_status()
                product_details = response.json()  

                for product_data in products_data:
                    product_id = product_data['id']
                    quantity = product_data['quantity']
                    product_detail = next((product for product in product_details if product['id'] == product_id), None)
                    if product_detail:
                        sale_data = {
                            'id': product_id,
                            'quantity': quantity,                        }
                        sales_data.append(sale_data)
                    else:
                        return Response(f"Product with ID {product_id} not found", status=status.HTTP_404_NOT_FOUND)
            except requests.exceptions.RequestException as e:
                return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            sale_serializer = SaleSerializer(data=sales_data, many=True)
            if sale_serializer.is_valid():
                sale_serializer.save()
                return Response(sale_serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(sale_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(sale_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def sales_report(request):
    try:
        sales = Sale.objects.all()
        sale_serializer = SaleSerializer(sales, many=True)

        products_data = sale_serializer.data
        product_ids = ','.join([str(product_data['id']) for product_data in products_data])

        product_url = f"http://localhost:3001/inventorys/by-ids/?ids={product_ids}"
        response = requests.get(product_url)
        response.raise_for_status()
        product_data_with_details = response.json()

        total_sales_count = 0
        total_sales_price = Decimal(0)
        product_sales = defaultdict(int)

        for sale_data in products_data:
            product_id = sale_data['id']
            product_quantity = sale_data['quantity']
            product_info = product_data_with_details.get(str(product_id))
            if product_info:
                product_name = product_info.get('name')
                product_price = Decimal(product_info.get('price', 0))
                total_sales_count += product_quantity
                total_sales_price += product_quantity * product_price
                product_sales[product_name] += product_quantity

        best_selling_product_name = max(product_sales, key=product_sales.get)

        response_data = {
            'total_sales_count': total_sales_count,
            'total_sales_price': round(total_sales_price, 2),
            'best_selling_product_name': best_selling_product_name,
        }

        return Response(response_data, status=200)

    except requests.exceptions.RequestException as e:
        return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
