from django.contrib import admin
from django.contrib.auth.models import User

# Register your models here.

from musker.models import Musker

admin.site.register(Musker)

#Extend user model

class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ['username']

admin.site.unregister(User)

admin.site.register(User, UserAdmin)