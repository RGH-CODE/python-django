from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.contenttypes.models import ContentType
from store.models import Product,Collection,Order,OrderItem
from django.db import transaction
from tag.models import TagItem

def htmlRender(request):
    #Transaction: to to execute two seperate logic/code and if one fails leads to both fail .and prevents us from unnecessary orders/error/
    #;;........let here is code that does not related to ordering product
    with transaction.atomic():
        order=Order()
        order.customer_id=1
        order.save()
        
        item=OrderItem()
        item.order=order
        item.product_id=1
        item.quantity=1
        item.unit_price=10
        item.save()
    return render(request,'hello.html',{'name':'Rajesh'})
    