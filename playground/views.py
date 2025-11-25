from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q,F
from store.models import Product,OrderItem

def htmlRender(request):
   #selecting related objects:prefetch_related(for many instance relationship)
   #eg product has many promotions
    queryset=Product.objects.prefetch_related('promotions').all()
   

    return render(request,'hello.html',{'name':'Rajesh','products':list(queryset)})
    
