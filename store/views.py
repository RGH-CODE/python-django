from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.db.models import Count
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from . models import Product,Customer,Collection,OrderItem
from . serializers import  ProductSerializer,CollectionSerializer


class ProductViewSet(ModelViewSet):
  queryset=Product.objects.all()
  
  
  serializer_class=ProductSerializer
  
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
   
  



