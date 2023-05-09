from django.shortcuts import render
from django.http import HttpResponse
from .models import Profile

#IMport json response
from django.http import JsonResponse
# Create your views here.

def home(request):
    return HttpResponse("Hello, world. You're at the musker index.")

def profile_list(request):
    profiles = Profile.objects.all()
    profiles_serialized = [profile.serialize() for profile in profiles]
    return JsonResponse(profiles_serialized, safe=False)

def profile_detail(request, pk):
    profile = Profile.objects.get(pk=pk)
    followers = profile.follows.all()
    followers_serialized = [follower.serialize() for follower in followers]
    print(profile.date_modified)    
    try:
        profile = Profile.objects.get(pk=pk)
    except Profile.DoesNotExist:
        return JsonResponse({"error": "Profile not found"}, status=404)
    return JsonResponse(profile.serialize())

   