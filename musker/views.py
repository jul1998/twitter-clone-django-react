from django.shortcuts import render
from django.http import HttpResponse
from .models import Profile, Meep

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
    try:
        profile = Profile.objects.get(pk=pk)
    except Profile.DoesNotExist:
        return JsonResponse({"error": "Profile not found"}, status=404)

    meeps = Meep.objects.filter(user_id=pk).values()

    data = {
        "profile": profile.serialize(),
        "meeps": list(meeps),
    }

    return JsonResponse(data)


def show_meeps(request):
    meeps = Meep.objects.all()
    meeps_serialized = [meep.serialize() for meep in meeps]
    return JsonResponse(meeps_serialized, safe=False)