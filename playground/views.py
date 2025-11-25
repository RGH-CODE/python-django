from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q,F
from store.models import Product

def htmlRender(request):
#     #sorting data
#     #1.sorts in alphabet ascending in title
#     queryset=Product.objects.order_by("title")
    
#     #2.sorts in alphabet descending in title
#     queryset=Product.objects.order_by("-title")
    
#     #3.unit price in ascending and title in descending
#     queryset=Product.objects.order_by("unit_price","-title")
   
#    #3.unit price in descending and title in ascending ...due to use of reverse()
    
#     queryset=Product.objects.order_by("unit_price","-title").reverse()
#     #return render(request,'hello.html',{'name':'Rajesh','products':list(queryset)})
    

#     #4.get individual object
#     product=Product.objects.order_by("unit_price")[0]
    
    
#     #use of earliest:sorts in ascending and returns first object
    
    product=Product.objects.earliest("unit_price")
#use of latest:sorts in descending and returns first object
    
    product=Product.objects.latest("unit_price")
    
    
   
    
   
    return render(request,'hello.html',{'name':'Rajesh','product':product})
    
