from rest_framework import serializers
from decimal import Decimal
from django.db import transaction
from . models import Product,Customer,Collection,Review,Cart,CartItem,Order,OrderItem
class CollectionSerializer(serializers.ModelSerializer):
    products_count=serializers.IntegerField(read_only=True)
    class Meta:
        model=Collection
        fields=['id','title','products_count']
       
        
       
    
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=['id','title','description','slug','inventory','price','price_with_tax','collection','collection_url']
    #since id and title are same name in product model they can be removed from here 
    price=serializers.DecimalField(max_digits=6,decimal_places=2,source='unit_price') #price name is not in product model so need to define here  
   
    #creating custom serializers fields
    price_with_tax=serializers.SerializerMethodField(method_name='calculate_tax') #it is not in product model
    
    def calculate_tax(self,product:Product):
        return product.unit_price * Decimal(1.1)
    #serializing using hyperlink:
    collection_url=serializers.HyperlinkedRelatedField(source='collection',view_name="collection-detail",read_only=True) #it is kept here cause we want collection in hyperlink form.But we can remove it if we want collection in primary key from
    collection = serializers.PrimaryKeyRelatedField(queryset=Collection.objects.all(),write_only=True)#for posting collection in pk/integer 




class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model=Review
        fields=['id','date','name','description']
        
        
    def create(self,validated_data):
            product_id=self.context['product_id']
            return Review.objects.create(product_id=product_id,**validated_data)

#for simple product detail
class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=['id','title','unit_price']

       
class CartItemSerializer(serializers.ModelSerializer):
    product=SimpleProductSerializer()
    total_price=serializers.SerializerMethodField()  
    
    def get_total_price(self,cart_item:CartItem):
        return cart_item.quantity*cart_item.product.unit_price
    
    class Meta:
        model=CartItem
        fields=['id','product','quantity','total_price']   
        
    
        
class CartSerializer(serializers.ModelSerializer):
    id=serializers.UUIDField(read_only=True)
    items=CartItemSerializer(many=True,read_only=True)
    
     
    total_price = serializers.SerializerMethodField()
        
    def get_total_price(self, cart):
        return sum(item.quantity * item.product.unit_price for item in cart.items.all())
       
    class Meta:
        model=Cart
        fields=['id','items','total_price']
        
        
class AddCartItemSerializer(serializers.ModelSerializer):
    product_id=serializers.IntegerField()
    
    def validate_product_id(self,value):
        if  not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError('No product with given id was found!!')
        return value
    
    def save(self,**kwargs):
        cart_id=self.context['cart_id']
        product_id=self.validated_data['product_id']
        quantity=self.validated_data['quantity']
        
        try:
           cart_item=CartItem.objects.get(cart_id=cart_id,product_id=product_id)
           cart_item.quantity+=quantity
           cart_item.save()
           self.instance=cart_item
           
        except CartItem.DoesNotExist:
            self.instance=CartItem.objects.create(cart_id=cart_id,**self.validated_data)
        return self.instance           
    class Meta:
        model=CartItem
        fields=['id','product_id','quantity']
        
        
#serializer for updating Cart Item
class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=CartItem
        fields=['quantity']
        




class CustomerSerializer(serializers.ModelSerializer):
    user_id=serializers.IntegerField(read_only=True)
    class Meta:
      model=Customer
      fields=['id','user_id','phone','birth_date','membership']
      

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=OrderItem
        fields=['id','product','unit_price','quantity']  
      
class OrderSerializer(serializers.ModelSerializer):
    items=OrderItemSerializer(many=True)
    class Meta:
        model=Order
        fields=['id','customer','placed_at','payment_status','items']
        
        
class CreateOrderSerializer(serializers.Serializer):
    cart_id=serializers.UUIDField()
    with transaction.atomic():
      def save(self,**kwargs):
          (customer,created)=Customer.objects.get_or_create(user_id=self.context['user_id'])
          order=Order.objects.create(customer=customer)
          
          cart_items=CartItem.objects.filter(cart_id=self.validated_data['cart_id'])
          
          order_items=[OrderItem(      #item for item in cart_items
              order=order,
              product=item.product,
              unit_price=item.product.unit_price,
              quantity=item.quantity
              ) for item in cart_items]
          OrderItem.objects.bulk_create(order_items)
          
          Cart.objects.filter(pk=self.validated_data['cart_id']).delete()
          return order