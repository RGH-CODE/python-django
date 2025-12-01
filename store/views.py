from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
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
        return Response("ok")


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
@api_view()
def product_detail(request,id):
    product=get_object_or_404(Product,pk=id)
    serializer=ProductSerializer(product)
    return Response(serializer.data)

@api_view(['GET','POST'])
def collection_detail(request,pk):
    if request.method=='GET':
      collection=get_object_or_404(Collection,pk=pk)
      serializer=CollectionSerializer(collection)
      return Response(serializer.data)
    elif request.method=='POST':
        serializer=CollectionSerializer(data=request.data)
        return Response('collection is added!!')