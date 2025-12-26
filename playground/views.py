from django.shortcuts import render 
from django.core.mail import send_mail,mail_admins,BadHeaderError
from templated_mail.mail import BaseEmailMessage

def htmlRender(request):
    try:
     message=BaseEmailMessage(
         template_name='emails/hello.html',
         context={'name':'Rajesh'}
         
     )
     
     message.send(['rajesh@gmail.com'])
    
    except BadHeaderError:
        pass
    
    return render(request,'hello.html',{'name':'Rajesh'})
    
      
    
    