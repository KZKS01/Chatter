from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class Post(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   content = models.TextField(max_length=300)
   created_at = models.DateTimeField(auto_now_add=True)
   likes = models.ManyToManyField(User, 'liked_posts')

   def get_absolute_url(self):
      return reverse('posts_index')
   
class Photo(models.Model):
   url = models.CharField(max_length=200)
   post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='photo')

   def __str__(self):
      return f'photo for post_id: {self.post_id} @{self.url}'