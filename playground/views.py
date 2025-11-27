from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.contenttypes.models import ContentType
from store.models import Product,Collection
from tag.models import TagItem

def htmlRender(request):
    #creating objects
    collection=Collection()
    collection.title="Digital gadgets"
    collection.featured_product=Product(pk=1)
    collection.save()
    collection.id
    
    return render(request,'hello.html',{'name':'Rajesh'})
    
