from django.urls import path, include
from foodgram.views import SignUp, index, user_page, feed, recipe_page, new_recipe, edit_recipe, favorites, wishlist


urlpatterns = [
    path('auth/', include('django.contrib.auth.urls')),
    path('auth/singup/', SignUp.as_view(), name='index'),
    path('', index, name='index'),
    path('feed/', feed, name='feed'),
    path('new/', new_recipe, name='new'),
    path('favorites/', favorites, name='favorites'),
    path('wishlist/', wishlist, name='wishlist'),
    path('<username>/', user_page, name='user'),
    path('<username>/<int:recipe_id>/', recipe_page, name='recipe'),
    path('<username>/<int:recipe_id>/edit/', edit_recipe, name='edit_recipe'),
]