from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name="index"),
    path("profile_list/", views.profile_list, name="profile_list"),
    path("profile/<int:pk>/", views.profile_detail, name="profile_detail"),
    path("meeps/", views.show_meeps, name="show_meeps"),
]