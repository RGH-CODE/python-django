from django.contrib import admin
from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html,urlencode
from .import models

#customization +register


#for product 
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=['title','unit_price','inventory_status','collection_title']
    list_editable=['unit_price']
    list_per_page=10
    list_select_related=['collection']
    list_filter=['collection','last_update']
   #for collection title
    def collection_title(self,product):
        return product.collection.title
       
   
    #for inventory status
    @admin.display(ordering='inventory')
    def inventory_status(self,product):
      if product.inventory<10:
        return 'Low'
      return 'Ok'

#for collection
@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
  list_display=['title','products_count']
  
  @admin.display(ordering='products_count')
  def products_count(self,collection):
    url=(reverse('admin:store_product_changelist')
         +'?'
         +urlencode({'collection_id':str(collection.id)}))
    return format_html('<a href={}>{}</a>',url,collection.products_count)
  
  #overriding product count.cause product count is not in model.py
  def get_queryset(self,request):
    return super().get_queryset(request).annotate(products_count=Count('products'))
  
    
  

#for customer 
@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display=['first_name','last_name','membership','orders_count']
    list_editable=['membership']
    list_per_page=10
    search_fields=['first_name__istartswith',"last_name__istartswith"]
    
    def get_queryset(self,request):
      return super().get_queryset(request).annotate(orders_count=Count('order'))
    
    @admin.display(ordering='orders_count',description="Orders")
    def orders_count(self,customer):
      url=(reverse(
        'admin:store_order_changelist'
      )
           +'?'
           +urlencode({
             'customer_id':customer.id
           }))
      return format_html('<a href={}>{}</a>',url,customer.orders_count)
#for order 
@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display=['id','customer','placed_at','payment_status']
    list_editable=['payment_status']
    