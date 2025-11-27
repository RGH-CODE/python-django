from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.contenttypes.models import ContentType
from store.models import Product,Collection
from tag.models import TagItem

def htmlRender(request):
    #deleting objects
    #1.to delete single known object
    '''
    collection=Collection(pk=11)
    collection.delete()
    '''
    #2.To delete multiple objects
    Collection.objects.filter(id__gt=8).delete()
    
    
    return render(request,'hello.html',{'name':'Rajesh'})
    