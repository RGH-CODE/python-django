from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.db.models import Count
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from . models import Product,Customer,Collection
from . serializers import  ProductSerializer,CollectionSerializer
# Create your views here.
# def product_list(request):
#This is django response
    #return HttpResponse('ok')
#better to use rest framework reponse which is better 
@api_view(['GET','POST'])
def product_list(request):
    if request.method=='GET':
      queryset=Product.objects.select_related('collection').all()
      serializer=ProductSerializer(queryset,many=True,context={'request':request})
      return Response(serializer.data)
    elif request.method=='POST':
        serializer=ProductSerializer(data=request.data) 
        #method 1 of checking validation of data
        # if serializer.is_valid():
        #     serializer.validated_data
        #     return Response('ok the data is deserialized!!')
        # else:
        #     return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST) #now if invalid data is posted then we get proper error
        
         #method 2 of checking validation of data
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.data)


# @api_view()
# def product_detail(request,id):
    # try:
    #   product=Product.objects.get(pk=id)
    #   serializer= ProductSerializer(product)
    #   return Response(serializer.data)
    # except Product.DoesNotExist:
    #     # return Response(status=404)
    #     #best way to do 
    #     return Response(status=status.HTTP_404_NOT_FOUND)
#but using try and catch for all time might be long so use django shortcuts
@api_view(["GET",'PUT','DELETE'])
def product_detail(request,id):
    product=get_object_or_404(Product,pk=id)
    if request.method=="GET":
      serializer=ProductSerializer(product,context={'request': request})
      return Response(serializer.data)
    elif request.method=="PUT":
      serializer=ProductSerializer(product,context={'request': request},data=request.data)
      serializer.is_valid(raise_exception=True)
      serializer.save()
      return Response(serializer.data)
    elif request.method=="DELETE":
      if product.orderitems.count()>0:
        return Response({'error':'This product can not be deleted cause it is related with order item'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
      product.delete()
      return Response({'Success':'Product deleted successfully'},status=status.HTTP_204_NO_CONTENT)
        

@api_view(["GET","POST"])
def collection_list(request):
  if request.method=="GET":
    queryset=Collection.objects.annotate(products_count=Count('products')).all()
    serializer=CollectionSerializer(queryset,many=True)
    return Response(serializer.data)
    
  elif request.method=="POST":
    serializer=CollectionSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)

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