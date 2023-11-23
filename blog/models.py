from django.db import models
from django.contrib.auth.models import User
import datetime

class Profile(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    bio=models.CharField(max_length=250,default='')
    img=models.ImageField(null=True,blank=True,default='johndoe.png')
    #img=models.CharField(default="johndoe.png", max_length=255)
    name=models.CharField(max_length=55,default='John Doe')
    

class Article(models.Model):
    author=models.ForeignKey(Profile,on_delete=models.CASCADE)
    likes=models.IntegerField(default=0)
    title=models.CharField(max_length=250)
    date=models.DateField(default=datetime.date.today)
    content=models.TextField()
    #img=models.CharField(null=True,blank=True,max_length=255)
    img=models.ImageField(null=True,blank=True)

class Likes(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    articleid=models.IntegerField()
    like=models.IntegerField(default=0) #1 if user liked
    
