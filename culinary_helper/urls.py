from django.urls import path
from .views import *


urlpatterns = [
    path('user/register/', register, name='register'),
    path('user/login/', login, name='login'),
    path('user/logout', logout, name='logout'),
    path('profile/edit/', edit_profile, name='edit_profile'),
]