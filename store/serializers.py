from rest_framework import serializers
from decimal import Decimal
from . models import Product,Customer,Collection
class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Collection
        fields=['id','title','featured_product']
    
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=['id','title','price','price_with_tax','collection']
    #since id and title are same name in product model they can be removed from here 
    price=serializers.DecimalField(max_digits=6,decimal_places=2,source='unit_price') #price name is not in product model so need to define here  
   
    #creating custom serializers fields
    price_with_tax=serializers.SerializerMethodField(method_name='calculate_tax') #it is not in product model
    
    def calculate_tax(self,product:Product):
        return product.unit_price * Decimal(1.1)
    #serializing using hyperlink:
    collection=serializers.HyperlinkedRelatedField(queryset=Collection.objects.all(),view_name="collection-detail") #it is kept here cause we want collection in hyperlink form.But we can remove it if we want collection in primary key from
    
