from django.db.models import Sum
from decimal import Decimal
from django.db.models import F




from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Sale
from .serializers import SaleSerializer

@api_view(['GET', 'POST'])
def sale_list(request):
    if request.method == 'GET':
        sales = Sale.objects.all()
        serializer = SaleSerializer(sales, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = SaleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def sales_report(request):
    total_sales = Decimal(0)
    for sale in Sale.objects.all():
        total_sales += sale.quantity * sale.price
    
    best_selling_product = Sale.objects.values('product_name').annotate(total_quantity=Sum('quantity')).order_by('-total_quantity').first()
    all_products = Sale.objects.values('product_name').annotate(total_quantity=Sum('quantity'), total_price=Sum(F('quantity') * F('price')))
    
    if best_selling_product:
        best_selling_product_name = best_selling_product['product_name']
        best_selling_product_quantity = best_selling_product['total_quantity']
    else:
        best_selling_product_name = None
        best_selling_product_quantity = 0

    return Response({
        'total_sales': round(total_sales, 2),
        'best_selling_product_name': best_selling_product_name,
        'best_selling_product_quantity': best_selling_product_quantity,
        'all_products': all_products
    })