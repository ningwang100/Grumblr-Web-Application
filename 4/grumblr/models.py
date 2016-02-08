from django.db import models
from django.contrib.auth.models import User


class Grumblr(models.Model):
    content = models.CharField(max_length=42)
    user = models.ForeignKey(User)
    title = models.CharField(max_length=100, default="", blank=True)
    time = models.DateTimeField(auto_now_add=True)
    liker = models.ManyToManyField(User,blank=True,related_name="+")

    def __unicode__(self):
        return self.content


class UserProfile(models.Model):
    user = models.OneToOneField(User,related_name="newuser")
    avatar = models.ImageField(upload_to='avatar')
    age = models.CharField(max_length=20)
    bio = models.CharField(max_length=420)
    token = models.CharField(max_length=100,default="")
    follow = models.ManyToManyField(User,blank=True,related_name="followed")

    def __unicode__(self):
        return self.avatar


