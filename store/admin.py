from django.contrib import admin
from .import models

#customization
class ProductAdmin(admin.ModelAdmin):
    list_display=['title','unit_price']
    list_editable=['unit_price']
    list_per_page=10


# Register your models here.


admin.site.register(models.Collection)
admin.site.register(models.Product,ProductAdmin)