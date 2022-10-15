from django.urls import path, include
from foodgram.views import index


urlpatterns = [
    path('auth/', include('django.contrib.auth.urls')),
    path('auth/singup/', index, name='index'),
]