from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from core.models import User
from store.admin import ProductAdmin
from store.models import Product
from tag.models import TagItem

@admin.register(User)
class UserAdmin(BaseUserAdmin):
   add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2","email","first_name","last_name"),
            },
        ),
    )
  
  
#inline for Tag
class TagedInline(GenericTabularInline):
  autocomplete_fields=['tag']
  model=TagItem
  extra=0
  
class CustomProductAdmin(ProductAdmin):
    inlines=[TagedInline]


# Register your models here.
admin.site.unregister(Product)
admin.site.register(Product,CustomProductAdmin)