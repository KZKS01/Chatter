from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class Post(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   content = models.TextField(max_length=300)
   created_at = models.DateTimeField(auto_now_add=True)
   likes = models.ManyToManyField(User, 'liked_posts')