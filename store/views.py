from django.shortcuts import render
from django.shortcuts import get_object_or_404

from django.db.models import Count

from rest_framework.response import Response
from rest_framework import status

from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet,GenericViewSet

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser

from rest_framework.mixins import CreateModelMixin,RetrieveModelMixin,DestroyModelMixin,UpdateModelMixin

from store.permissions import AdminOrReadOnly, ViewCustomerHistoryPermission

from . models import Product,Customer,Collection,OrderItem, ProductImage,Review,Cart,CartItem,Order
from . serializers import  ProductImageSerializer, ProductSerializer,CollectionSerializer,ReviewSerializer,CartSerializer,CartItemSerializer,AddCartItemSerializer,UpdateCartItemSerializer,CustomerSerializer,OrderSerializer,CreateOrderSerializer,UpdateOrderSerializer
from . filters import ProductFilter
from . pagination import DefaultPagination


class ProductViewSet(ModelViewSet):
  queryset=Product.objects.prefetch_related('images').all()
  serializer_class=ProductSerializer
  filter_backends=[DjangoFilterBackend,SearchFilter,OrderingFilter]
  filterset_class=ProductFilter
  pagination_class=DefaultPagination
  search_fields=['title','description']
  ordering_fields=['unit_price','last_update']
  permission_classes=[AdminOrReadOnly]
  
  
  def get_serializer_context(self):
      return {'request':self.request}
  
  
  
  def destroy(self,request ,*args,**kwargs):
      if OrderItem.objects.filter(product_id=kwargs['pk']).count()>0:
        return Response({'error':'This product can not be deleted cause it is related with order item'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
      return super().destroy(request,*args,**kwargs)
    
    #'''#->we implemented above destroy function instead of this below cause we can only product detail to allow deleted not product list .this destroy function is built in function '''
    # def delete(self,request,pk):
    #   product=get_object_or_404(Product,pk=pk)
    #   if product.orderitems.count()>0:
    #     return Response({'error':'This product can not be deleted cause it is related with order item'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
    #   product.delete()
    #   return Response({'Success':'Product deleted successfully'},status=status.HTTP_204_NO_CONTENT)
        
  
  
  
#Building viewset to related class collectionlist and collectiondetail
class CollectionViewSet(ModelViewSet):
   queryset=Collection.objects.annotate(products_count=Count('products')).all()
   serializer_class=CollectionSerializer
  
   def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminUser()]
      
      
   def destroy(self ,request,*args,**kwargs):
      if OrderItem.objects.filter(product_id=kwargs['pk']).count()>0:
        return Response({'error':'This collection can not be deleted cause it is related with order item'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
      return super().destroy(request,*args,**kwargs)
  
  
  #  def delete(self,request,id):
  #     collection=get_object_or_404(Collection,pk=pk)
  #     if collection.products.count()>0:
  #       return Response({'Error':'This collection cannot be deleted cause it contaions more than one product!!'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
  #     collection.delete()
  #     return Response({f'Success':'collection {id} is deleted successfully'},status=status.HTTP_204_NO_CONTENT) 
   
  


class ReviewViewSet(ModelViewSet):
  #queryset=Review.objects.all() #this is correct but it shows same review for different product so add logic by function
  def get_queryset(self):
    return Review.objects.filter(product_id=self.kwargs['product_pk'])
  serializer_class=ReviewSerializer
  
  def get_serializer_context(self):
    return {'product_id':self.kwargs['product_pk']}
  
  
#CARTVIEWSET
class CartViewSet(CreateModelMixin,GenericViewSet,RetrieveModelMixin,DestroyModelMixin):
  queryset=Cart.objects.prefetch_related('items__product').all()
  serializer_class=CartSerializer
  



#cartitemviewset 
class CartItemViewSet(ModelViewSet):
  http_method_names=['get','post','patch','delete']
  def get_serializer_class(self):
    if self.request.method=="POST":
      return AddCartItemSerializer
    
  
    elif self.request.method=="PATCH":
      return UpdateCartItemSerializer
    return CartItemSerializer
  
  def get_serializer_context(self):
    return {'cart_id':self.kwargs['cart_pk']}
    
    
    
  def get_queryset(self):
    return CartItem.objects.filter(cart_id=self.kwargs['cart_pk']).select_related('product')
  
  
  
#for customer
class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes=[IsAdminUser]
    
    @action(detail=True,permission_classes=[ViewCustomerHistoryPermission])
    def history(self,request,pk):
      return Response("you have permission to view")
    

    @action(detail=False,methods=["get","put"],permission_classes=[IsAuthenticated])
    def me(self,request):
      customer=Customer.objects.get(user_id=request.user.id)
      if request.method=="GET":
        serializer=CustomerSerializer(customer)
        return Response(serializer.data)
      
      elif request.method=="PUT":
        serializer=CustomerSerializer(customer,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
      

class OrderViewSet(ModelViewSet):
  http_method_names=['get','patch','delete','head','options']
  def get_permissons(self):
    if self.request.method in ['PATCH','DELETE']:
      return[IsAdminUser()]
    return[IsAuthenticated]
    
    
    
  def create(self,request,*args,**kwargs):
    serializer=CreateOrderSerializer(data=request.data,context={'user_id':self.request.user.id})
    serializer.is_valid(raise_exception=True)
    order=serializer.save()
    serializer=OrderSerializer(order)
    return Response(serializer.data)
  
  
  def get_serializer_class(self):
    if self.request.method=='POST':
      return CreateOrderSerializer
    elif self.request.method=='PATCH':
      return UpdateOrderSerializer
    return OrderSerializer
 
  

  def get_queryset(self):
    if self.request.user.is_staff:
      return Order.objects.all()
    customer_id=Customer.objects.get(user_id=self.request.user.id)
    Order.objects.filter(customer_id=customer_id)
    
class ProductImageViewSet(ModelViewSet):
  serializer_class=ProductImageSerializer
  
  def get_queryset(self):
    return ProductImage.objects.filter(product_id=self.kwargs['product_pk'])
  
  def get_serializer_context(self):
    return {'product_id':self.kwargs['product_pk']}