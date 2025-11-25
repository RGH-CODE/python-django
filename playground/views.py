from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q,F
from store.models import Product

def htmlRender(request):
    #Limiting results
    #1.we get product upto 5 from 0 to 4
    queryset=Product.objects.all()[:5]

    #2.we get product upto 5 from 5to 10
    queryset=Product.objects.all()[5:10]




    return render(request,'hello.html',{'name':'Rajesh','products':list(queryset)})
    
