from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q,F
from store.models import Product,OrderItem

def htmlRender(request):
   #selecting related objects:select_related(for one instance relationship)
    #1.it selects the query from product with collection.this select_related prevents from generating extra query
    #Note select_related is used for one instance relation ie here product has one collection.
    queryset=Product.objects.select_related('collection').all()
   #2.to expand relation we use:
    #queryset=Product.objects.select_related('collection__SomeOtherField').all()
   

    return render(request,'hello.html',{'name':'Rajesh','products':list(queryset)})
    
