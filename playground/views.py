from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from store.models import Product
#filtering methods
def htmlRender(request):
   #complex filter/lookups using Q objects
   #1.products:inventory<10 or unit price <20
    queryset = Product.objects.filter(Q(inventory__lt=10) | Q(unit_price__lt=20))
    
    #2.products:inventory<10 and  unit price not <20
    queryset = Product.objects.filter(Q(inventory__lt=10) & ~Q(unit_price__lt=20))

   
    return render(request,'hello.html',{'name':'Rajesh','products':list(queryset)})
    
