from django.contrib import admin
from .models import Post, Photo, UserProfile, Comment, Like

# Register your models here.
admin.site.register([Post, Photo, UserProfile, Comment, Like])