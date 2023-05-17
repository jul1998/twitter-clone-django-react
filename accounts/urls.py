from django.urls import path, include, re_path

from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path("update_user/", views.update_user, name="update_user")
]
