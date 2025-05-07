from django.db import models
import uuid
from django.contrib.auth.models import User
# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=500)
    artist = models.CharField(max_length=500,null=True)
    url = models.URLField(max_length=500,null=True)
    image = models.URLField(max_length=500)
    author = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name='posts')
    body = models.TextField() 
    tags = models.ManyToManyField('Tag')
    created = models.DateTimeField(auto_now_add=True)
    id = models.CharField(primary_key=True, default=uuid.uuid4, editable=False)
    
    def __str__(self):
        return str(self.title)
    class Meta:
        ordering = ['-created']
        
class Tag(models.Model):
    name = models.CharField(max_length=20)
    image = models.FileField(upload_to='icons/',null=True,blank=True)
    
    slug = models.SlugField(max_length=20,unique=True)
    order = models.IntegerField(null=True)
    
    def __str__(self):
        return str(self.name)
    class Meta:
        ordering = ['-order']