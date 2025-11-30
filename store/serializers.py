from rest_framework import serializers
from decimal import Decimal
from . models import Product,Customer,Collection
class CollectionSerializer(serializers.Serializer):
    id=serializers.IntegerField()
    title=serializers.CharField(max_length=255)
class ProductSerializer(serializers.Serializer):
    id=serializers.IntegerField()
    title=serializers.CharField(max_length=255)
    price=serializers.DecimalField(max_digits=6,decimal_places=2,source='unit_price')
   
    #creating custom serializers fields
    price_with_tax=serializers.SerializerMethodField(method_name='calculate_tax')
    
    #serializing using hyperlink:
    collection=serializers.HyperlinkedRelatedField(queryset=Collection.objects.all(),view_name="collection-detail")
    def calculate_tax(self,product:Product):
        return product.unit_price * Decimal(1.1)
    
