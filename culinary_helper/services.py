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


def save_profile_changes(context, avatar, about: str, gender):
    """Сохранение данных профиля пользователя"""
    context.user_profile.avatar = avatar 
    context.user_profile.about = about
    context.user_profile.gender = gender
    context.user_profile.save()