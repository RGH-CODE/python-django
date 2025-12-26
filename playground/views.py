from django.shortcuts import render 
from django.core.mail import send_mail,mail_admins,BadHeadError

def htmlRender(request):
    try:
     send_mail('subject','message','from@rajesh.com',['rajesh@gmail.com'])
    
    except BadHeadError:
        pass
    
    return render(request,'hello.html',{'name':'Rajesh'})
    
      
    
    