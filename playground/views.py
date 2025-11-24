from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from store.models import Product
#filtering methods
def htmlRender(request):
    #1.get objects having price range b/w 20-30
    #->queryset=Product.objects.filter(unit_price__range=(20,30))
    
    #2.get product that has greater than one collection
    #->queryset=Product.objects.filter(collection__id__gt=1)
    
    #3.get products that title starts with coffee
    #->queryset=Product.objects.filter(title__icontains="coffee")#icontains to make case insensitive
    
    #4.get products that title starts with letter m
    #-> queryset=Product.objects.filter(title__istartswith="m")
    
    #5.
    #queryset=Product.objects.filter(last_update__year=2021)
     
    #6.to check product without description
    queryset = Product.objects.filter(description__isnull=True)

   
    return render(request,'hello.html',{'name':'Rajesh','products':list(queryset)})
    
