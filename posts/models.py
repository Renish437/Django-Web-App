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

class Comment (models.Model):
    author = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name='comments')
    parent_post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    body = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    id = models.CharField(max_length=100,default=uuid.uuid4,unique=True,primary_key=True,editable=False)
    
    def __str__(self):
        try:
            return f'Comment by {self.author.username} on {self.parent_post.title}'
        except:
            return f'Comment by no author on {self.parent_post}'
        
    class Meta:
        ordering = ['-created']

class Reply(models.Model):
    author = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name='replies')
    parent_comment = models.ForeignKey(Comment,on_delete=models.CASCADE,related_name='replies')
    body = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    id = models.CharField(max_length=100,default=uuid.uuid4,unique=True,primary_key=True,editable=False)
    
    def __str__(self):
        try:
            return f'Reply by {self.author.username} on {self.parent_comment.body}'
        except:
            return f'Reply by no author on {self.parent_comment}'
        
    class Meta:
        ordering = ['created']