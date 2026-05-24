from rest_framework import serializers
from decimal import Decimal
from django.db import transaction

from . models import Product,Customer,Collection, ProductImage,Review,Cart,CartItem,Order,OrderItem,Address
class CollectionSerializer(serializers.ModelSerializer):
    products_count=serializers.IntegerField(read_only=True)
    class Meta:
        model=Collection
        fields=['id','title','products_count']
       
        
class ProductImageSerializer(serializers.ModelSerializer):
    
    def create(self,validated_data):
        product_id=self.context['product_id']
        return ProductImage.objects.create(product_id=product_id,**validated_data)
        
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        if instance.image:
            rep['image'] = instance.image.url
        return rep
    
    class Meta:
        model=ProductImage
        fields=['id','image']
           
    
class ProductSerializer(serializers.ModelSerializer):
    images=ProductImageSerializer(many=True,read_only=True)
    class Meta:
        model=Product
        fields=['id','title','description','slug','inventory','price','price_with_tax','collection','collection_url','images']
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
    image = serializers.SerializerMethodField()
    class Meta:
        model=Product
        fields=['id','image','title','unit_price']
    
    def get_image(self,product):
        image=product.images.first()
        if image:
            return image.image.url
        return None
        
        

       
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
    product=SimpleProductSerializer(read_only=True)
    class Meta:
        model=OrderItem
        fields=['id','product','unit_price','quantity']  
    
    
class OrderSerializer(serializers.ModelSerializer):
    items=OrderItemSerializer(many=True,read_only=True)
    class Meta:
        model=Order
        fields=['id','customer','placed_at','payment_status','items']
        
        
class CreateOrderSerializer(serializers.Serializer):
    #cart checkout
    cart_id=serializers.UUIDField(required=False)
    
    #Buy-Now
    product_id=serializers.IntegerField(required=False)
    quantity=serializers.IntegerField(required=False,default=1)
    
    #main validation
    def validate(self,attrs):
        cart_id=attrs.get("cart_id")
        product_id=attrs.get("product_id")
        quantity=attrs.get("quantity",1)
        
    
    #provide one either cart or direct product 
    
        if not cart_id and not product_id:
           raise serializers.ValidationError("provide cart_id or product_id")
    
    
        if cart_id:
            if not Cart.objects.filter(pk=cart_id).exists():
                raise serializers.ValidationError({"cart_id":"cart not found!!"})
            
            if CartItem.objects.filter(cart_id=cart_id).count()==0:
                raise serializers.ValidationError({"cart_id":"cart is empty"})
            
    
        if product_id:
          if not Product.objects.filter(pk=product_id).exists():
            raise serializers.ValidationError({"product_id":"product not found!"})
        
          if quantity<=0:
            raise serializers.ValidationError({
                {"quantity":"Qunatity must be grater or equal to 1"}
            })
  
  
        customer=Customer.objects.get(user_id=self.context["user_id"])
        
        if not customer.phone:
            raise serializers.ValidationError({
                "phone":"please add phone number before placing order"
            })
            
        if not Address.objects.filter(customer=customer).exists():
            raise serializers.ValidationError({
               "address":"please add delivery address before placing order" 
            })
        return attrs
    
    def save(self,**kwargs):
       with transaction.atomic():
          customer=Customer.objects.get(user_id=self.context['user_id'])
          order=Order.objects.create(customer=customer)
          cart_id=self.validated_data.get("cart_id")
          product_id=self.validated_data.get("product_id")
          
          quantity=self.validated_data.get("quantity",1)
  
  
          #cart checkout
          if cart_id:
              cart_items=CartItem.objects.select_related("product").filter(cart_id=cart_id)
              order_items=[
                  OrderItem(
                     order=order,
                     product=item.product,
                     unit_price=item.product.unit_price,
                     quantity=item.quantity,
                      
                  )
                  for item in cart_items
                  
              ]
              OrderItem.objects.bulk_create(order_items)
  
              #delete cart after placing order 
              Cart.objects.filter(
                  pk=cart_id
              ).delete()
              
          #buy now checkout
          elif product_id:
              product=Product.objects.get(
                  pk=product_id
              )
              
              OrderItem.objects.create(
                  order=order,
                  product=product,
                  unit_price=product.unit_price,
                  quantity=quantity
              )
              return order
               
    
    
    
class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields=['payment_status']
        
        
class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model=Address
        fields=['street','city','province','postal_code']
        