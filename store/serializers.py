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
    
    #1.method one of serializing relationship which returns collection id/int
    #->collection=serializers.PrimaryKeyRelatedField(queryset=Collection.objects.all())
    
    #2.method two serializing relationship which returns collection title
    #->collection=serializers.StringRelatedField() #takes long load so go to views.product_list->queryset and add select_related('collection)
    
    #3.method third using collection serializers
    collection=CollectionSerializer()
    def calculate_tax(self,product:Product):
        return product.unit_price * Decimal(1.1)
    
