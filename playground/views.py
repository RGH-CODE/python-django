from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q,F
from store.models import Product,OrderItem

def htmlRender(request):
   #Selecting flields to query
    #1.we get id and title in dictionary from
    queryset=Product.objects.values('id','title')

    #1.we get id and title and title of collection  in dictionary from
    queryset=Product.objects.values('id','title','collection__title')

    #1.we get id and title and title of collection  in tuple from
    queryset=Product.objects.values_list('id','title','collection__title')

    #.Select products that have been order and sort them by title
    queryset=Product.objects.filter(id__in=OrderItem.objects.values('product_id').distinct()).order_by('title')



    return render(request,'hello.html',{'name':'Rajesh','products':list(queryset)})
    
