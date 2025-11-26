from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q,F
from store.models import Product,OrderItem,Order

def htmlRender(request):
    #Get the last 5 orders with their customer and items(including products)
    queryset=Order.objects.select_related('customer').prefetch_related('orderitem_set__product').order_by('-placed_at')[:5]
   

    return render(request,'hello.html',{'name':'Rajesh','orders':list(queryset)})
    
