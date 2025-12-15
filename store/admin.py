from django.contrib import admin
from .import models

#customization +register


#for product 
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=['title','unit_price']
    list_editable=['unit_price']
    list_per_page=10

#for collection
admin.site.register(models.Collection)

#for customer 
@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display=['first_name','last_name','membership']
    list_editable=['membership']
    list_per_page=10