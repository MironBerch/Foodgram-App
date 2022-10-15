from django.contrib import admin
from foodgram.models import Recipe, Ingredient, RecipeIngredient, Follow, Favorites, Wishlist


admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(RecipeIngredient)
admin.site.register(Follow)
admin.site.register(Favorites)
admin.site.register(Wishlist)