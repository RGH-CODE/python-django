from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.contenttypes.models import ContentType
from store.models import Product,Collection,Order,OrderItem
from django.db import transaction
from django.db import connection 
from tag.models import TagItem

def htmlRender(request):
    #Executing Rw sql queries
    #1.method one 
    #->queryset=Product.objects.raw('SELECT * FROM store_product') #for all fields
    #->queryset=Product.objects.raw('SELECT id,title FROM store_product') #for all fields
    
    # #2.method two 
    # cursor=connection.cursor()
    # cursor.execute('SELECT id,title FROM store_product')
    # cursor.close()
    
    # #3.method three:it closes cursor automatically 
    # with Connection.cursor() as cursor:
    #     cursor.execute('SELECT id,title FROM store_product')
        
    #4.for store prodcedure :using callproc procedure
    # with connection.cursor() as cursor:
    #     cursor.callProc('get_customer',[1,2])
        #it does not support in pymysql
    
    return render(request,'hello.html',{'name':'Rajesh','result':list(queryset)})
    
      
    
    