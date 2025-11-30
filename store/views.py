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
@api_view()
def product_list(request):
    queryset=Product.objects.select_related('collection').all()
    serializer=ProductSerializer(queryset,many=True,context={'request':request})
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
@api_view()
def product_detail(request,id):
    product=get_object_or_404(Product,pk=id)
    serializer=ProductSerializer(product)
    return Response(serializer.data)

@api_view()
def collection_detail(request,pk):
    collection=get_object_or_404(Collection,pk=pk)
    serializer=CollectionSerializer(collection)
    return Response(serializer.data)
