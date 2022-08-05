from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth import authenticate
#from .models import
from django.contrib.auth.decorators import login_required


