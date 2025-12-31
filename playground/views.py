from django.shortcuts import render 
from .tasks import notify_customer

def htmlRender(request):
    notify_customer.delay('Hello')
    return render(request,'hello.html',{'name':"Rajesh"})
    