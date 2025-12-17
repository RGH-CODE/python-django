from django.contrib import admin,messages
from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html,urlencode

from .import models



#Additional Admin Filter 
class InventoryFilter(admin.SimpleListFilter):
  title='inventory'
  parameter_name='inventory'
  
  def lookups(self,request,model_admin):
    return [('<10','Low'),
            ('>10','Bet(11-50)'),
            ('>100','High')]
  
  def queryset(self,request,queryset:QuerySet):
    if self.value()=='<10':
     return queryset.filter(inventory__lt=10)
    if self.value()=='>10':
      return queryset.filter(inventory__lt=50 , inventory__gt=10)
    elif self.value()=='>100':
      return queryset.filter(inventory__gt=100)
    
    

#customization +register
#for product 
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    exclude=['promotions']
    prepopulated_fields={
      'slug':['title']
    }
    autocomplete_fields=['collection']
    actions=['clear_inventory']
    list_display=['title','unit_price','inventory_status','collection_title']
    
    list_editable=['unit_price']
    list_per_page=10
    list_select_related=['collection']
    list_filter=['collection','last_update',InventoryFilter]
    search_fields=['title']
   #for collection title
    def collection_title(self,product):
        return product.collection.title
       
   
    #for inventory status
    @admin.display(ordering='inventory')
    def inventory_status(self,product):
      if product.inventory<10:
        return 'Low'
      return 'Ok'
    
    #for clearing inventory
    @admin.action(description="Clear Inventory")
    def clear_inventory(self,request,queryset):
      updated_count=queryset.update(inventory=0)
      
      self.message_user(
        request,
        f'{updated_count} Products were updated successfully',
        messages.ERROR 
      )
    
    
#for collection
@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
  list_display=['title','products_count']
  search_fields=['title']
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
    
    
#for children inline orderitem for order 
class OrderItemInline(admin.TabularInline): #we can use stackedinline instead of tabularinline 
  autocomplete_fields=['product']
  model=models.OrderItem
  extra=0 #removing unfilled tables 
  min_num=1
  max_num=10
  

#for order 
@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields=['customer']
    inlines=[OrderItemInline]
    list_display=['id','customer','placed_at','payment_status']
    list_editable=['payment_status']
    