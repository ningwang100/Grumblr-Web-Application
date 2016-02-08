from django.db import models
from django.contrib.auth.models import User


class Grumblr(models.Model):
    content = models.CharField(max_length=42)
    user = models.ForeignKey(User)
    title = models.CharField(max_length=100, default="", blank=True)
    time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.content


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    photopath = models.CharField(max_length=150)
    def __unicode__(self):
        return self.photopath


# class UserProfile(models.Model):
#     user = models.OneToOneField(User)
#     photopath = models.CharField(max_length=150)
#
# User.profile=property(lambda u: UserProfile.objects.get_or_create(user=u)[0])