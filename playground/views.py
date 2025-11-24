from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from store.models import Product
# Create your views here.
#it is plain text 

#     return HttpResponse("Hello Rajesh")
#this is render using template
#retrieving objects methods
#1.objects.all
# def htmlRender(request):
#     query_set=Product.objects.all()
#     for product in query_set:
#         print(product)
#     return render(request,'hello.html',{'name':'Rajesh'})
#2.objects.get(pk=1) django selects pk as id
def htmlRender(request):
    try:
       query_set=Product.objects.get(pk=0) #if i provide invalid id/pk then get method returns error so to handle this we wrap this in exception handling
    except ObjectDoesNotExist:
        print("Object not found!!")
    return render(request,'hello.html',{'name':'Rajesh'})
    
    