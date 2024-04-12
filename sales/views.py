from decimal import Decimal
from django.http import JsonResponse
from collections import defaultdict
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Sale, Product
from .serializers import SaleSerializer, ProductSerializer
import requests


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer

    def list(self, request, *args, **kwargs):

        return super().list(request, *args, **kwargs)

    
@api_view(['GET'])
def sales_statistics(request):

    total_vendido = 0
    for sale in Sale.objects.all():
        total_vendido += sale.total()

    total_vendas = Sale.objects.all().count()

    produtos_vendidos = {}
    for sale in Sale.objects.all():
        for product in sale.produtos.all():
            if product.id_produto not in produtos_vendidos:
                produtos_vendidos[product.id_produto] = 0
            produtos_vendidos[product.id_produto] += product.quantity

    produto_mais_vendido_id = max(produtos_vendidos, key=produtos_vendidos.get)
    produto_mais_vendido = Product.objects.filter(id_produto=produto_mais_vendido_id).first()

    return Response({
        'total_vendido': total_vendido,
        'total_vendas': total_vendas,
        'produto_mais_vendido': {
            'id_produto': produto_mais_vendido.id_produto,
            'quantidade_vendida': produtos_vendidos[produto_mais_vendido_id]
        }
    })