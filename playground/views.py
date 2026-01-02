from django.shortcuts import render 
import requests
from django.core.cache import cache 
def htmlRender(request):
    key='httpbin_result'
    if cache.get(key) is None:
       response=requests.get('https://httpbin.org/delay/2')
       data=response.json()
       cache.set(key,data)
    return render(request,'hello.html',{'name':cache.get(key)})
    