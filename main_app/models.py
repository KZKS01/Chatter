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
   likes = models.ManyToManyField(User, 'liked_posts')

   def get_absolute_url(self):
      return reverse('posts_index')
   
class Photo(models.Model):
   url = models.CharField(max_length=200)
   post = models.ForeignKey(Post, on_delete=models.CASCADE)

   def __str__(self):
      return f'photo for post_id: {self.post_id} @{self.url}'
   
class UserProfile(models.Model):
   user = models.OneToOneField(User, on_delete=models.CASCADE)
   avatar = models.ImageField(upload_to='avatars/', default='avatars/default_avatar.png')
   bio = models.TextField(max_length=100)

   def __str__(self):
      return self.user.username

   # registers a signal receiver fn
   # post_save signal is sent by Django after a model instance is saved, the signal is triggered whenever a User model instance is saved
   @receiver(post_save, sender=User)
   # signal receiver fn that is called whenever a User instance is saved
   # sender param specifies the model class that sends the signal (User model)
   # instance param: the actual instance of the User model that was saved
   # created param: a boolean flag that indicates whether the instance was newly created (as opposed to being updated).
   # **kwargs: handle any additional arguments that may be passed to the post_save signal
   def create_profile(sender, instance, created, **kwargs):
      if created: # checks whether the created flag is True
         # creates a one-to-one relationship between the User and UserProfile models
         UserProfile.objects.create(user=instance)


   @receiver(post_save, sender=User)
   def save_profile(sender, instance, **kwargs):
      print("Creating profile for user")
      # updates the UserProfile instance associated with the User instance that was just saved
      # by calling .save() on the UserProfile instance's profile attr, which is a reference to the associated User instance
      instance.userprofile.save()