from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate
from .models import *
from django.http import Http404


def registration_user_and_profile(request, username: str, email: str, password: str) -> None:
    """Создание пользователя, его аунтификация и регистрация профиля пользователя"""
    user = User.objects.create_user(username=username, email=email, password=password)
    user.save()

    user_login = auth.authenticate(username=username)
    auth.login(request, user_login)

    user_model = User.objects.get(username=username)
    new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
    new_profile.save()


def search_profile(request): 
    try:
        user_profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        raise Http404
    context = {
        'user_profile': user_profile
    }
    return context