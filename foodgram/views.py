from django.shortcuts import render
from django.views.generic import CreateView
from django.urls import reverse_lazy
from foodgram.forms import CreationForm
from foodgram.helper import tag_collect


class SignUp(CreationForm):
    """SignUp view class"""
    form_class = CreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


def index(request):
    tags, tags_filter = tag_collect(request)