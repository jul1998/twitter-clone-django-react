from django.shortcuts import render, get_object_or_404
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
    

def like_meep(request):
    data = json.loads(request.body)
    print(data)
    user_id = data.get("user_id", "")
    meep_id = data.get("meep_id", "")
    meep = get_object_or_404(Meep, id=meep_id)
   
    if meep.likes.filter(id=user_id).exists():
        meep.likes.remove(user_id)
        return JsonResponse({"message": "Meep unliked successfully."}, status=201)

    else:
        meep.likes.add(user_id)
        return JsonResponse({"message": "Meep liked successfully."}, status=201)

def get_likes_count(request):
    try:
        data = json.loads(request.body)
        meep_id = data.get("meep_id", "")
        meep = get_object_or_404(Meep, id=meep_id)
        likes_count = meep.total_likes()
        return JsonResponse({"likes_total": likes_count}, status=201)
    except Exception as e:
        print(e)
        return JsonResponse({"error": str(e)}, status=500)