from django.urls import path, include
from foodgram.views import index


urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('singup/', index, name='index'),
]