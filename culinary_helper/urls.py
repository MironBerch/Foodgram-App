from django.urls import path
from .views import *


urlpatterns = [
    path('user/register/', register, name='register'),
    path('user/login/', login, name='login'),
    path('user/logout', logout, name='logout'),
    path('profile/settings/', profile_edit, name='profile_settings'),
    #path('profile/view/<int:id>', profile_view, name='view'),
    path('recipe/create/', recipe_create, name='recipe_create'),
    path('profile/view/<str:pk>', profile_view, name='profile_view'),
    path('profile_follow/', profile_follow, name='profile_follow'),
    path('recipe/feed/', recipe_feed, name='recipe_feed'),
]