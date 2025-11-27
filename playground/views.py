from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.contenttypes.models import ContentType
from store.models import Product,Collection
from tag.models import TagItem

def htmlRender(request):
    #creating objects
    #1.method 1 of updating
    '''
    collection=Collection(pk=11)
    collection.title="Games"
    collection.featured_product=None
    collection.save()
    '''
   
   #probelm of using method 1 for updating here we forget to indicaate title so django sets title to empty which leads to dataloss
    '''collection=Collection(pk=11)
   
    collection.featured_product=None
    collection.save()
    '''
    #2. method 2 of updating update. which solves problem of data loss in database 
    Collection.objects.filter(pk=11).update(featured_product=None)
    return render(request,'hello.html',{'name':'Rajesh'})
    