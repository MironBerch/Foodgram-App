from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth import authenticate
from .models import *
from django.contrib.auth.decorators import login_required
from .services import registration_user_and_profile, save_profile_changes
from django.http import Http404
from django.views.generic import ListView, DetailView
from django.db.models import F


def register(request):
    """Функция регистрации пользователя и профиля пользователя"""
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Почта занята')
                return redirect('register')

            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Имя пользователя занято')
                return redirect('register')
            
            else:
                registration_user_and_profile(request, username, email, password)
                return redirect(login)

        else:
            messages.info(request, 'Пароль не подходит')
            return redirect('register')
    
    else:
        return render(request, 'culinary_helper/user/register.html')


def login(request):
    """Вход в аккаунт"""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')

        else:
            messages.info(request, 'Не правильная почта или пароль')
            return redirect('login')

    else:
        return render(request, 'culinary_helper/user/login.html')


@login_required(login_url='login')
def logout(request):
    """Выход из аккаунта"""
    auth.logout(request)
    return redirect('login')


@login_required(login_url='login')
def profile_edit(request):
    """Изменение профиля пользователя"""
    try:
        user_profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        raise Http404
    context = {
        'user_profile': user_profile
    }

    if request.method == 'POST':
        if request.FILES.get('avatar') == None:
            avatar = user_profile.avatar
            about = request.POST['about']
            gender = request.POST['gender']

            save_profile_changes(user_profile, avatar, about, gender)

        if request.FILES.get('avatar') != None:
            avatar = request.FILES.get('avatar')
            about = request.POST['about']
            gender = request.POST['gender']

            save_profile_changes(user_profile, avatar, about, gender)

        messages.info(request, 'Settings save')
        return redirect('settings')
        

    return render(request, 'culinary_helper/profile/settings.html', context)


@login_required(login_url='login')
def recipe_create(request):
    if request.method == 'POST':
        user = request.user.username
        title = request.POST['title']
        preview = request.FILES.get('preview')
        text = request.POST['text']
        type = request.POST['type']
        complexity = request.POST['complexity']

        recipe = Recipe.objects.create(user=user, title=title, preview=preview, text=text, type=type, complexity=complexity)
        recipe.save()

        return redirect('/')
    
    return render(request, 'culinary_helper/recipe/create.html')


#def profile_view(request):
#    user_object = 