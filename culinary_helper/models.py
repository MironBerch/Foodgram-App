from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
import uuid
from datetime import datetime
from django.urls import reverse
from django import forms


class Profile(models.Model):
    """Модель профиля"""
    GENDER = (
        ('male', 'male'),
        ('female', 'female')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    gender = models.CharField(max_length=6, choices=GENDER, default='male')
    about = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='profile_avatars/', default='default_avatar.png')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профиля'


class Follower(models.Model):
    """Модель последователя"""
    follower = models.CharField(max_length=50)
    user = models.CharField(max_length=50)

    def __str__(self):
        return self.user

    class Meta:
        verbose_name = 'Подписчик'
        verbose_name_plural = 'Подписчики'


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
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    title = models.CharField(max_length=100)
    user = models.CharField(max_length=50)
    #url = models.SlugField(max_length=100, unique=True)
    preview = models.ImageField(upload_to='preview/')
    #preview_text = models.CharField(max_length=255, blank=True)
    text = models.TextField()
    type = models.CharField(max_length=5, choices=TYPE_OF_DISH, default='full')
    complexity = models.CharField(max_length=6, choices=DIFFICULTY_LEVEL, default='normal')
    views = models.IntegerField(default=0)
    lovers = models.IntegerField(default=0)

    def __str__(self):
        return self.user

    #def get_absolute_url(self):
    #    return reverse('recipe_detail', kwargs={'slug': self.url})

    def get_review(self):
        return self.recipereviews_set.filter(parent__isnull=True)

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class LoveRecipe(models.Model):
    '''Модель отметки понравилось'''
    recipe_url = models.CharField(max_length=100)
    username = models.CharField(max_length=100)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Отметка нравится'
        verbose_name_plural = 'Отметки нравится'


class RecipeReviews(models.Model):
    """Модель комментария к рецепту"""
    recipe = models.ForeignKey(Recipe, verbose_name='Рецепт', on_delete=models.CASCADE)
    username = models.CharField(max_length=100)
    text = models.TextField(max_length=550)
    parent = models.ForeignKey('self', verbose_name='Родитель', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f'{self.username} - {self.recipe}'

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'