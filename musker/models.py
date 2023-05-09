from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

#Create a user profile model

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField('self', related_name='followed_by', symmetrical=False, blank=True)
    date_modified = models.DateTimeField(User, auto_now=True)

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