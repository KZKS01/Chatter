from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models.signals import post_save #import a post_save signal sent to django when a user is created
from django.dispatch import receiver # import the receiver, specify the fn that will be executed when certain signals are sent 

# Create your models here.
class Post(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   content = models.TextField(max_length=300)
   created_at = models.DateTimeField(auto_now_add=True)
   comment_num = models.IntegerField(default=0)
   likes = models.ManyToManyField(User, 'liked_posts')

   def get_absolute_url(self):
      return reverse('posts_index')

   def increment_comment_num(self):
      self.comment_num += 1
      self.save(update_fields=['comment_num'])
   
   def decrement_comment_num(self):
      self.comment_num -= 1
      self.save(update_fields=['comment_num'])
   
class Photo(models.Model):
   url = models.CharField(max_length=200)
   post = models.ForeignKey(Post, on_delete=models.CASCADE)

   def __str__(self):
      return f'photo for post_id: {self.post_id} @{self.url}'
   
class UserProfile(models.Model):
   user = models.OneToOneField(User, on_delete=models.CASCADE)
   avatar = models.CharField(max_length=200, default='https://s3.us-east-2.amazonaws.com/k-chatter/713d6b.PNG')
   bio = models.TextField(max_length=100)

   def __str__(self):
      return self.user.username
   
class Comment(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   post = models.ForeignKey(Post, on_delete=models.CASCADE)
   content = models.TextField(max_length=300)
   created_at = models.DateTimeField(auto_now_add=True)

   def get_absolute_url(self):
      return reverse('post_detail', kwargs={'post_id': self.post_id})