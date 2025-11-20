from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
# Create your models here.

class Tag(models.Model):
    label=models.CharField(max_length=255)
    
class TagItem(models.Model):
    #What tag applied to what object 
    tag=models.ForeignKey(Tag,on_delete=models.CASCADE)
    
    #to apply Generic Relationship we need three fields 1.content_type(product,audio,video), 2.object_id, 3.content_object
    content_type=models.ForeignKey(ContentType,on_delete=models.CASCADE)
    object_id=models.PositiveIntegerField()
    content_object=GenericForeignKey()



