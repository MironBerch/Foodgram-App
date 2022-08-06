from django.urls import path
from .views import *


urlpatterns = [
    path('user/register/', register, name='register'),
    path('user/login/', login, name='login'),
    path('user/logout', logout, name='logout'),
    path('profile/settings/', profile_edit, name='settings'),
    #path('profile/view/<int:id>', profile_view, name='view')
]