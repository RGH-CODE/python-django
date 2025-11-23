from django.db import models

# Create your models here.
class Collection(models.Model):
    title=models.CharField(max_length=255)
    featured_product=models.ForeignKey('Product',on_delete=models.SET_NULL,null=True,related_name='+')#we do 'Product' cause Product class in defined below this class but in comming future it is not going to rename easily to solve we created related_name='+' so that django does not create reverse relation between product and collection classes.
#many to many relationship between promotion-product 
class Promotion(models.Model):
    description=models.CharField(max_length=255)
    discount=models.FloatField()
    
    
class Product(models.Model):
    title=models.CharField(max_length=250)
    slug=models.SlugField()
    description=models.TextField()
    unit_price=models.DecimalField(max_digits=6,decimal_places=2)
    inventory=models.IntegerField()
    last_update=models.DateTimeField(auto_now=True)
    collection=models.ForeignKey(Collection,on_delete=models.PROTECT) #one to many relationship with collection  to product class 
    promotions=models.ManyToManyField(Promotion)
class Customer(models.Model):
    MEMBERSHIP_BRONZE='B'
    MEMBERSHIP_SILVER='S'
    MEMBERSHIP_GOLD='G'
    
    MEMBERSHIP_CHOICES=[
        (MEMBERSHIP_BRONZE,'Bronze'),
        (MEMBERSHIP_SILVER,'Silver'),
        (MEMBERSHIP_GOLD,'Gold'),
    ]
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=40)
    email=models.EmailField(unique=True)
    phone=models.PositiveIntegerField(max_length=20)
    birth_date=models.DateField(null=True)
    membership=models.CharField(max_length=1,choices=MEMBERSHIP_CHOICES,default=MEMBERSHIP_BRONZE)  
    
    
class Order(models.Model):
    PAYMENT_STATUS_PENDING='P'
    PAYMENT_STATUS_COMPLETE='C'
    PAYMENT_STATUS_FAILED='F'
    PAYMENT_STATUS_CHOICES=[
        (PAYMENT_STATUS_PENDING,'pending'),
        (PAYMENT_STATUS_COMPLETE,'complete'),
        (PAYMENT_STATUS_FAILED,'failed'),
    ]
    placed_at=models.DateTimeField(auto_now_add=True)  
    payment_status=models.CharField(max_length=1,choices=PAYMENT_STATUS_CHOICES,default=PAYMENT_STATUS_PENDING)
    customer=models.ForeignKey(Customer,on_delete=models.PROTECT)
#one to one relationship with address to  customer  class 
class Address(models.Model):
    street=models.CharField(max_length=255)
    city=models.CharField(max_length=255)
    customer=models.OneToOneField(Customer,on_delete=models.CASCADE,primary_key=True) #one to ONE relationship with customer  to address class 
    
class OrderItem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.PROTECT) #one to many relationship with Order  to OrderItem class 
    product=models.ForeignKey(Product,on_delete=models.PROTECT)  #one to many relationship with cart  to OrderItem class 
    quantity=models.PositiveSmallIntegerField()
    unit_price=models.DecimalField(max_digits=6,decimal_places=2)
class Cart(models.Model):
    created_at=models.DateTimeField(auto_now_add=True)
    
class CartItem(models.Model):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveSmallIntegerField()
    
    


