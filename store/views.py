from django.shortcuts import render
from django.shortcuts import get_object_or_404

from django.db.models import Count

from rest_framework.response import Response
from rest_framework import status

from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter

from rest_framework.mixins import CreateModelMixin,RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet

from . models import Product,Customer,Collection,OrderItem,Review,Cart
from . serializers import  ProductSerializer,CollectionSerializer,ReviewSerializer,CartSerializer
from . filters import ProductFilter
from . pagination import DefaultPagination


class ProductViewSet(ModelViewSet):
  queryset=Product.objects.all()
  serializer_class=ProductSerializer
  filter_backends=[DjangoFilterBackend,SearchFilter,OrderingFilter]
  filterset_class=ProductFilter
  pagination_class=DefaultPagination
  search_fields=['title','description']
  ordering_fields=['unit_price','last_update']
  
  
  
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
class CartViewSet(CreateModelMixin,GenericViewSet,RetrieveModelMixin):
  queryset=Cart.objects.prefetch_related('items__product').all()
  serializer_class=CartSerializer
  
