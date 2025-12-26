from django.shortcuts import render 
from django.core.mail import send_mail,mail_admins,BadHeaderError

def htmlRender(request):
    try:
     mail_admins('subject','message',html_message='this is admin mail')
    
    except BadHeaderError:
        pass
    
    return render(request,'hello.html',{'name':'Rajesh'})
    
      
    
    