from django.contrib import admin
from .models import *


admin.site.register(Profile)
admin.site.register(Follower)
admin.site.register(Recipe)
admin.site.register(LikeRecipe)
admin.site.register(RecipeReviews)