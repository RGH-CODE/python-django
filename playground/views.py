from django.shortcuts import render 
import requests
def htmlRender(request):
    requests.get('https://httpbin.org/delay/2')
    return render(request,'hello.html',{'name':"Rajesh"})
    