from django.shortcuts import render 
from django.core.mail import send_mail,mail_admins,BadHeaderError,EmailMessage

def htmlRender(request):
    try:
     message=EmailMessage('subject','message','from@rajesh.com',['rajesh@gmail.com'])
     message.attach_file('playground/static/images/abc.jpg')
     message.send()
    
    except BadHeaderError:
        pass
    
    return render(request,'hello.html',{'name':'Rajesh'})
    
      
    
    