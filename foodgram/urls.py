from django.urls import path
from foodgram.views import index


urlpatterns = [
    path('', index, name='index'),
]