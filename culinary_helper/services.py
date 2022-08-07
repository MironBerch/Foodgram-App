from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate
from .models import *
from django.http import Http404
from .views import *


def registration_user_and_profile(request, username: str, email: str, password: str):
    """Создание пользователя, его аунтификация и регистрация профиля пользователя"""
    user = User.objects.create_user(username=username, email=email, password=password)
    user.save()

    user_login = auth.authenticate(username=username, password=password)
    auth.login(request, user_login)

    user_model = User.objects.get(username=username)
    new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
    new_profile.save()


def save_profile_changes(user_profile, avatar, about: str, gender):
    """Сохранение данных профиля пользователя"""
    user_profile.avatar = avatar 
    user_profile.about = about
    user_profile.gender = gender
    user_profile.save()


def collecting_profile_information(request, pk) :
    """Сбор информации профиля"""
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_recipe = Recipe.objects.filter(user=pk)
    user_recipe_quantity = len(user_recipe)
    
    follower = request.user.username
    user = pk

    if Follower.objects.filter(follower=follower, user=user).first():
        user_follow_button = 'Unfollow'
    else:
        user_follow_button = 'Follow'

    user_following = len(Follower.objects.filter(follower=pk))
    user_followers = len(Follower.objects.filter(user=pk))

    profile_info_list = [user_object, user_profile, user_recipe, user_recipe_quantity, user_follow_button, user_following, user_followers]
    
    return profile_info_list 



def processing_subscription_form(follower:str, user:str):
    """Обработка формы подписки на профиль"""
    if Follower.objects.filter(follower=follower, user=user).first():
        delete_follower = Follower.objects.get(follower=follower, user=user)
        delete_follower.delete()

    else:
        new_follower = Follower.objects.create(follower=follower, user=user)
        new_follower.save()