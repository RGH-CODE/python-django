from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q,F
from django.db.models.aggregates import Count,Max,Min,Avg,Sum
from store.models import Product,OrderItem,Order

def htmlRender(request):
    #aggregating objects
    result=Product.objects.aggregate(Count('id'))
    #proper way of showing
    result=Product.objects.aggregate(count=Count('id'))
    
    #to aggregate multiple fields 
    result=Product.objects.aggregate(count=Count('id'),Minimum_price=Min('unit_price'))
    
    #below code selects the product whose collection id is 1 and computes two aggregates value i.e min price and id 
    result=Product.objects.filter(collection__id=1).aggregate(count=Count('id'),Minimum_price=Min('unit_price'))
    


    return render(request,'hello.html',{'name':'Rajesh','result':result})
    
