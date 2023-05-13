from django.contrib import admin
from django.contrib.auth.models import User

# Register your models here.
from .models import Profile, Meep, MeepForm

# Mix profile into User info

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profiles'

#Extend user model

class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ['username']
    inlines = [ProfileInline]

admin.site.unregister(User)

admin.site.register(User, UserAdmin)
admin.site.register(Meep)

#admin.site.register(Profile)

