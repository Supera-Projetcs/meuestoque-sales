from rest_framework import serializers
from .models import Sale, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class SaleSerializer(serializers.ModelSerializer):
    produtos = ProductSerializer(many=True)

    class Meta:
        model = Sale
        fields = '__all__'

    def create(self, validated_data):
        produtos_data = validated_data.pop('produtos')
        sale = Sale.objects.create(**validated_data)
        for produto_data in produtos_data:
            product = Product.objects.create(**produto_data)
            sale.produtos.add(product)
        return sale
