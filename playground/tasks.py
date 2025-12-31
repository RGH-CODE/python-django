from time import sleep 
#from storefront.celery import celery #it creates dependency with our main app which we dont want 
from celery import shared_task #so we used this method 

@shared_task
def notify_customer(message):
    print("sending 1k emails...")
    print(message)
    sleep(10)
    print("Emails were send successfully!!!")
    
# @celery.task.  #This method creates depedency with storefront app so not recommanded 
# def notify_customer(message):
#     print("sending 1k emails...")
#     print(message)
#     sleep(10)
#     print("Emails were send successfully!!!")

