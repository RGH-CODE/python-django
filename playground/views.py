from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q,F
from store.models import Product,OrderItem

def htmlRender(request):
   #selecting related objects:prefetch_related(for many instance relationship) and select_related(for one instance)ie combine selection of objects
   
    queryset=Product.objects.prefetch_related('promotions').select_related('collection').all()
   

    return render(request,'hello.html',{'name':'Rajesh','products':list(queryset)})
    
