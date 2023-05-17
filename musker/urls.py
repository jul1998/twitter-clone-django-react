from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name="index"),
    path("profile_list/", views.profile_list, name="profile_list"),
    path("profile/<int:pk>/", views.profile_detail, name="profile_detail"),
    path("meeps/", views.show_meeps, name="show_meeps"),
    path("meeps/<int:user_id>/", views.show_meeps_by_user_id, name="show_meeps_by_user_id"),
    path("create_meep/", views.create_meep, name="create_meep"),
    path("like_meep/", views.like_meep, name="like_meep"),
    path("likes_count/", views.get_likes_count, name="get_likes_count"),
]