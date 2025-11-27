from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.contenttypes.models import ContentType
from store.models import Product 
from tag.models import TagItem

def htmlRender(request):
    content_type=ContentType.objects.get_for_model(Product)
    queryset=TagItem.objects.select_related('tag').filter(content_type=content_type,object_id=1)
    return render(request,'hello.html',{'name':'Rajesh','orders':list(queryset)})
    
