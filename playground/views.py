from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q,F,Value,Func
from django.db.models.functions import Concat 
from store.models import Product,OrderItem,Order,Customer

def htmlRender(request):
   #Annotating Objects:to add additional attributes to objects while quering them 
    # queryset=Customer.objects.annotate(is_new=True) #we get error cause we cannot pass booelan we need to pass expression like 1.value 2.F 3.Aggregate
    #to solve this 
    #1.Value =for simple value
    queryset=Customer.objects.annotate(is_new=Value(True))
    
    #to create new attribute same as id of customer can be done by F object referencing related flieds 
    queryset=Customer.objects.annotate(new_id=F('id'))
    
    #to create new attribute same as id of customer increasing each by 1 can be done by F object referencing related flieds 
    queryset=Customer.objects.annotate(new_id=F('id')+1)
    
    #Calling Database Functions using Func
    queryset=Customer.objects.annotate(full_name=Func(F('first_name'),Value(' '), F('last_name'),function='CONCAT'))
    
    #shortcut way of concatinating using cancat function
    queryset=Customer.objects.annotate(full_name=Concat('first_name',Value(' '), 'last_name'))

    return render(request,'hello.html',{'name':'Rajesh','orders':list(queryset)})
    
