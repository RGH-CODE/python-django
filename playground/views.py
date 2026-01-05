from django.shortcuts import render 
import requests
from rest_framework.views import APIView
import logging


logger=logging.getLogger(__name__) #playground.views
class HelloView(APIView):
 def get(self,request):
  try:
    logger.info('calling httpbin')
    response=requests.get('https://httpbin.org/delay/2')
    logger.info('Received httpbin')
    data=response.json()  
  except requests.ConnectionError:
     logger.critical('httpbin is offline')
  return render(request,'hello.html',{'name':'Rajesh'})
    