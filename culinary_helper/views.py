from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth import authenticate
from .models import *
from django.contrib.auth.decorators import login_required
from .services import registration_user_and_profile, save_profile_changes, processing_subscription_form, collecting_profile_information #,transformation_of_like_form
from django.http import Http404
from django.db.models import F
from itertools import chain


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
        return redirect('profile_settings')
        

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


@login_required(login_url='login')
def profile_view(request, pk):

    profile_info_objects = collecting_profile_information(request, pk)

    context = {
        'user_object': profile_info_objects[0],
        'user_profile': profile_info_objects[1],
        'user_recipe': profile_info_objects[2],
        'user_recipe_quantity': profile_info_objects[3],
        'user_follow_button': profile_info_objects[4],
        'user_following': profile_info_objects[5],
        'user_followers': profile_info_objects[6],
    }

    return render(request, 'culinary_helper/profile/view.html', context)


@login_required(login_url='login')
def profile_follow(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']

        processing_subscription_form(follower, user)
        return redirect('/profile/view/' + user)

    else:
        return redirect('/')


@login_required(login_url='login')
def recipe_feed(request):

    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    recipes = Recipe.objects.all()
    context = {
        'user_profile': user_profile,
        'recipes': recipes,
    }

    return render(request, 'culinary_helper/recipe/feed.html', context)


@login_required(login_url='login')
def recipe_detail_view(request):
    username = request.user.username
    recipe_id = request.GET.get('recipe_id')
    recipe = Recipe.objects.get(id=recipe_id)
    
    context = {
        'recipe': recipe,
    }

    return render(request, 'culinary_helper/recipe/detail_view.html', context)


@login_required(login_url='login')
def processing_like_mark(request):
    username = request.user.username
    recipe_id = request.GET.get('recipe_id')
    recipe = Recipe.objects.get(id=recipe_id)
    like_filter = LikeRecipe.objects.filter(recipe_id=recipe_id, username=username)
    if like_filter == None:
        new_like = LikeRecipe.objects.create(recipe_id=recipe_id, username=username)
        new_like.save()
        recipe.likes = recipe.likes+1
        recipe.save()
    else:
        like_filter.delete()
        recipe.likes = recipe.likes-1
        recipe.save()
    return redirect('/recipe/view/' + recipe_id)