from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
#it is plain text 

#     return HttpResponse("Hello Rajesh")
#this is render using template
def htmlRender(request):
    return render(request,'hello.html',{'name':'Rajesh'})
    