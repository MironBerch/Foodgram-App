from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
import uuid


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField(max_length=1000)
    avatar = models.FileField(upload_to='avarats/')


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=50)
    text = models.TextField()