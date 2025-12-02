from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.db.models import Count
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from . models import Product,Customer,Collection
from . serializers import  ProductSerializer,CollectionSerializer

#creating  class for generic view 
# ->class ProductList(ListCreateAPIView):
#   def get_queryset(self):
#     return Product.objects.select_related('collection').all()
  
#   def get_serializer_class(self):
#     return ProductSerializer
  
#   def get_serializer_context(self):
#     return {'request':self.request}
    
  #if function has no special logic then you can simply create/assign parameter like
class ProductList(ListCreateAPIView):
  
    queryset=Product.objects.select_related('collection').all()
  
  
    serializer_class=ProductSerializer
  
    def get_serializer_context(self):
      return {'request':self.request}
  
  
  
#creating  class for class based view 

#creating generic view for product detail using retrieveupdatedestroyapiview
class ProductDetail(RetrieveUpdateDestroyAPIView):
  queryset=Product.objects.all()
  serializer_class=ProductSerializer
  
  def delete(self,request,pk):
      product=get_object_or_404(Product,pk=pk)
      if product.orderitems.count()>0:
        return Response({'error':'This product can not be deleted cause it is related with order item'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
      product.delete()
      return Response({'Success':'Product deleted successfully'},status=status.HTTP_204_NO_CONTENT)
        



class CollectionList(ListCreateAPIView):
    
    queryset=Collection.objects.annotate(products_count=Count('products')).all()
    serializer_class=CollectionSerializer
   
    
 
@api_view(['GET','PUT','DELETE'])
def collection_detail(request,pk):
    collection=get_object_or_404(Collection.objects.annotate(product_count=Count('products')),pk=pk)
    if request.method=='GET':
      serializer=CollectionSerializer(collection)
      return Response(serializer.data)
    elif request.method=='PUT':
        serializer=CollectionSerializer(collection,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method=='DELETE':
      if collection.products.count()>0:
        return Response({'Error':'This collection cannot be deleted cause it contaions more than one product!!'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
      collection.delete()
      return Response({f'Success':'collection {id} is deleted successfully'},status=status.HTTP_204_NO_CONTENT)