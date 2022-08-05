from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
import uuid
from datetime import datetime
from django.urls import reverse


class Profile(models.Model):
    """Модель профиля"""
    GENDER = (
        ('male', 'male'),
        ('female', 'female')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_id = models.IntegerField()
    user_gender = models.CharField(max_length=6, choices=GENDER, dedault='male')
    user_about = models.TextField(blank=True, null=True)
    user_avatar = models.ImageField(upload_to='profile_avatars/', default='default_avatar.png')

    def __str__(self):
        return self.user.username


class Follower(models.Model):
    """Модель последователя"""
    follower = models.CharField(max_length=50)
    user = models.CharField(max_length=50)

    def __str__(self):
        return self.user


class Recipe(models.Model):
    """Модель рецепта"""
    TYPE_OF_DISH = (
        ('full', 'full'),
        ('snack', 'snack'),
        ('drink', 'drink')
    )
    DIFFICULTY_LEVEL = (
        ('easy', 'easy'),
        ('normal', 'normal'),
        ('hard', 'hard')
    )
    title = models.CharField(max_lengt=100)
    user = models.CharField(max_length=50)
    url = models.SlugField(max_lengt=100, unique=True)
    preview = models.CharField(upload_to='preview/')
    #preview_text = models.CharField(max_length=255, blank=True)
    text = models.TextField()
    type = models.CharField(max_length=5, choices=TYPE_OF_DISH, default='full')
    complexity = models.CharField(max_length=6, choices=DIFFICULTY_LEVEL, default='normal')
    views = models.IntegerField(default=0)
    lovers = models.IntegerField(default=0)

    def __str__(self):
        return self.user

    def get_absolute_url(self):
        return reverse("recipe_detail", kwargs={"slug": self.url})

    def get_review(self):
        return self.recipereviews_set.filter(parent__isnull=True)

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class LoveRecipe(models.Model):
    '''Модель отметки понравилось'''
    recipe_url = models.CharField(max_length=100)
    username = models.CharField(max_lengt=100)

    def __str__(self):
        return self.username


class RecipeReviews(models.Model):
    """Модель комментария к рецепту"""
    recipe = models.ForeignKey(Recipe, verbose_name='Рецепт')
    username = models.CharField(max_length=100)
    text = models.TextField(max_length=550)
    parent = models.ForeignKey('self', verbose_name='Родитель', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f'{self.username} - {self.recipe}'

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'