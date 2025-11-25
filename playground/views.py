from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q,F
from store.models import Product
#filtering methods
def htmlRender(request):
   #Referencing Fileds Using F objects
    #1.products has has same inventory number as unit price 
    queryset=Product.objects.filter(inventory=F('unit_price'))
     #2.products has has same inventory number as collection id 
    queryset=Product.objects.filter(inventory=F('collection__id'))
    return render(request,'hello.html',{'name':'Rajesh','products':list(queryset)})
    
