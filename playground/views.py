from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.contenttypes.models import ContentType
from store.models import Product 
from tag.models import TagItem

def htmlRender(request):
    #querying generic relationships 
    queryset=TagItem.objects.get_tags_for(Product,1)
    return render(request,'hello.html',{'name':'Rajesh','orders':list(queryset)})
    
