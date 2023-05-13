from django.shortcuts import render
from django.http import HttpResponse
from .models import Profile, Meep
import json

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
    meeps = Meep.objects.all().order_by('-created_at')
    meeps_serialized = [meep.serialize() for meep in meeps]
    return JsonResponse(meeps_serialized, safe=False)

def show_meeps_by_user_id(request, user_id):
    meeps = Meep.objects.filter(user_id=user_id)
    meeps_serialized = [meep.serialize() for meep in meeps]
    return JsonResponse(meeps_serialized, safe=False )

def create_meep(request):
    if request.method == "POST":
        data = json.loads(request.body)
        body = data.get("body", "")
        user_id = data.get("user_id", "")
        if user_id is None or user_id == "":
            return JsonResponse({"error": "user_id required."}, status=400)
        
        if body is None or body == "":
            return JsonResponse({"error": "body required."}, status=400)
        
        try:
            meep = Meep(body=body, user_id=user_id)
           
        except:
            return JsonResponse({"error": "Error creating meep."}, status=400)
        else:
            meep.save()
            return JsonResponse({"message": "Meep created successfully."}, status=201)
    else:
        return JsonResponse({"error": "POST request required."}, status=400)