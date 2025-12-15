from django.contrib import admin
from .import models

#customization +register


#for product 
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=['title','unit_price','inventory_status','collection_title']
    list_editable=['unit_price']
    list_per_page=10
    list_select_related=['collection']
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
admin.site.register(models.Collection)

#for customer 
@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display=['first_name','last_name','membership']
    list_editable=['membership']
    list_per_page=10