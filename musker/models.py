from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

#Create a user profile model

# create meep model
class MeepForm(models.Model):
    body = models.CharField(max_length=280)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, default=None)
    
    def __str__(self):
        return self.body
    
    def serialize(self):
        return {
            "body": self.body,
        }
    

class Meep(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    body = models.CharField(max_length=280)
    created_at = models.DateTimeField(User, auto_now=True)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)

    # Keep track of likes
    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.body
    
    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "body": self.body,
            "date_modified": self.created_at.strftime("%b %d %Y, %I:%M %p"), # "Feb 14 2020, 3:25 PM
        }

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField('self', related_name='followed_by', symmetrical=False, blank=True)
    date_modified = models.DateTimeField(User, auto_now=True)
    profile_image = models.ImageField(upload_to='profile_images', blank=True, null=True)

    def __str__(self):
        return self.user.username
    
    def serialize(self):
        follows_list = list(self.follows.values('id', 'user__username'))
        return {
            "id": self.id,
            "user": self.user.username,
            "follows": follows_list,
            "date_modified": self.date_modified.strftime("%b %d %Y, %I:%M %p"), # "Feb 14 2020, 3:25 PM
            "followed_by": list(self.followed_by.values('id', 'user__username')),
            "profile_image": self.profile_image.url if self.profile_image else None,

        }
    
# Create profile when new user signs up

def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile.objects.create(user=instance)
        user_profile.save()

        # Have the user follow themselves 
        user_profile.follows.set([instance.profile.id])
        user_profile.save()


post_save.connect(create_profile, sender=User)