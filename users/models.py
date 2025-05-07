from django.db import models
from django.contrib.auth.models import User
from django.templatetags.static import static
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='avatars/',null=True,blank=True)
    realname = models.CharField(max_length=100,null=True,blank=True)
    email = models.EmailField(unique=True,null=True)
    location = models.CharField(max_length=100,null=True,blank=True)
    bio = models.TextField(null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True)
   
    @property
    def name(self):
        if self.realname:
            name= self.realname
        else:
            name= self.user.username
        return name
    @property
    def avatar(self):
        if self.image:
            avatar = self.image.url
        else:
            avatar= static('images/avatar_default.png')
        return avatar
         
    