from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Post, Photo, User, UserProfile, Comment, Like
from django.db.models import Q # search fn: allows for complex queries using logical operators like &, |, and ~ (not)
import boto3
import uuid
from django.urls import reverse


S3_BASE_URL = 'https://s3.us-east-2.amazonaws.com/'
BUCKET = 'k-chatter'

def home(request):
    posts = Post.objects.all() # to be used in the html
    user = request.user
    return render(request, 'home.html', {
        'posts': posts,
        'user': user,
})

def user_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user_profile = UserProfile.objects.get(user=user)
    join_date = user.date_joined.strftime('%B %Y')
    followers_num = user_profile.followers_num()
    # reposts = Post.objects.filter(reposts__user=user_profile.user)
    posts = Post.objects.filter(user=user)
    username = user.username
    user_id = user.id

    return render(request, 'users/user_profile.html', {
        'user': user,
        'user_profile': user_profile,
        'followers_num': followers_num,
        'join_date': join_date,
        # 'reposts': reposts,
        'posts': posts,
        'username' : username,
        'user_id': user_id,
        'user': user,
})

# follwers
@login_required
def follow(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user_profile = get_object_or_404(UserProfile, user=user)
    follower = request.user
    
    if follower in user_profile.followers.all():
        user_profile.followers.remove(follower)
    else:
        user_profile.followers.add(follower)

    return redirect('user_profile', user_id=user_id)


class UserProfileEdit(LoginRequiredMixin, UpdateView):
    model = UserProfile
    fields = ('bio', )
    template_name = 'users/edit_user_profile.html'

    def get_success_url(self):
        user_id = self.kwargs['pk']
        return reverse('user_profile', kwargs={'user_id': user_id})


# AWS - Avatar Upload
@login_required
def add_avatar(request, user_id):
    avatar_file = request.FILES.get('avatar-file', None)

    if avatar_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + avatar_file.name[avatar_file.name.rfind('.'):]

    try:
        s3.upload_fileobj(avatar_file, BUCKET, key)
        url = f"{S3_BASE_URL}{BUCKET}/{key}"
        request.user.userprofile.avatar = url
        request.user.userprofile.save() # save the updated user profile

    except Exception as error:
        messages.error(request, f'Avatar upload failed: {error}')

    return redirect('user_profile', user_id=user_id)

def delete_avatar(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user_profile = get_object_or_404(UserProfile, user=user)

    s3 = boto3.client('s3')
    key = user_profile.avatar.split('/')[-1]

    try:
        s3.delete_object(Bucket=BUCKET, Key=key)
    except Exception as error:
        print(f'Avatar delete failed:{error}')


    user_profile.avatar = 'https://s3.us-east-2.amazonaws.com/k-chatter/713d6b.PNG'
    user_profile.save()
    return redirect('user_profile', user_id=user_id)


# SIGNUP 
def signup(request):
    # POST req: save users in db
    error_message = '' # declare it first to be overwritten
    if request.method == 'POST':
        # create a user in memory using UserCreationForm(to process and validate data)
        form = UserCreationForm(request.POST) # request.POST: the form data
        # check if form inputs are valid
        if form.is_valid():
            # if valid: save new user to db as 'user'
            user = form.save()
            # login the new user
            login(request, user)
            # Create a user profile for the newly signed up user
            UserProfile.objects.create(user=user, avatar='https://s3.us-east-2.amazonaws.com/k-chatter/713d6b.PNG')
            # redirect user to home pg
            return redirect('home')
        # if not valid: generate an err msg
        else: 
            error_message = 'Invalid sign up - please try again.'

    # GET req: sign up form
    form = UserCreationForm() # send an empty form to client
    return render(request, 'registration/signup.html', {
        'form': form, # passing form data
        'error': error_message,
    })



# Google OAuth
def signup_redirect(request):
    messages.error(request, 'This account already exist. Try login instead.')
    return redirect('login')


# POSTS
class PostCompose(LoginRequiredMixin, CreateView):
    model = Post
    fields = ('content',)
    template_name = 'posts/post_form.html' 

    # take validated inputs to create a model instance
    def form_valid(self, form):
        form.instance.user = self.request.user # associate the new post with the post creater
        # calls the parent class method form_valid and returns its result
        # the parent method saves the form data to the db & redirects to the success URL specified in the view
        super().form_valid(form)

        # call add_photo to create photos
        photo_file = self.request.FILES.get('photo-file')
        if photo_file:
            photo = add_photo(photo_file, self.object.pk)
            photo.post = self.get_object
            photo.save()

        return super().form_valid(form)


class PostEdit(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ('content', )
    template_name = 'posts/post_form.html'

    # parent class of the UpdateView
    # handling the incoming request and deciding which HTTP method (GET, etc.) to call depending on the req
    def dispatch(self, request, *args, **kwargs):
            # check if the user is allowed to edit the post
            if not self.edit_permission():
                return redirect('home')

            # if allow, all the parent class's dispatch method
            return super().dispatch(request, *args, **kwargs) # ensure that all the arguments are properly passed to the parent class's dispatch method

    def edit_permission(self):
        # get the object that this view is displaying.
        post = self.get_object()

        # check if the current user is the owner of the post.
        if not post.user == self.request.user:
            return False

        return True

class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = '/chatter/'
    template_name = 'posts/post_confirm_delete.html'


@login_required
def posts_index(request):
    posts = Post.objects.filter(user=request.user) # to be used in the html
    username = request.user.username
    user = request.user
    user_id = request.user.id
    return render(request, 'posts/posts_index.html', {
        'posts': posts, 
        'username' : username,
        'user_id': user_id,
        'user': user,
        })

@login_required
def post_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    user = request.user
    user_id = request.user.id
    comments = Comment.objects.filter(post=post_id)
    return render(request, 'posts/post_detail.html', {
        'post': post,
        'user': user,
        'user_id': user_id,
        'comments': comments,
        })

#reposts
@login_required
def repost(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user

    if user in post.reposts.all():
        post.reposts.remove(user)
        post.decrement_repost_num()
    else:
        post.reposts.add(user)
        post.increment_repost_num()

    return redirect('post_detail', post_id=post_id)



# search function
def search(request):
    user = request.user

    if request.method == 'GET':
        searching = request.GET.get('searching', None)

        if not searching: # if empty string
            return redirect('home')

        results = Post.objects.filter(
            Q(user__username__icontains=searching) |
            Q(content__icontains=searching)
        )

    else:
        results = []

    return render(request, 'posts/search.html', {
        'results': results,
        'searching': searching,
        'user': user,
    })

@login_required
# AWS - Photo Upload
def add_photo(request, post_id):# accepts an HTTP req obj and a cat_id integer param
    # attempt to collect photo submission from req
    # if file not found, None is returned and assigned to the var photo-file
    photo_file = request.FILES.get('photo-file', None)

    # if photo file present
    if photo_file:
        # set up a s3 client obj for working with AMZN s3
        s3 = boto3.client('s3')

        # create a UNIQUE name for the file with uuid
        # uuid.uuid4() fn generates a random UUID
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]

    # try upload file to aws s3 via s3.upload_fileobj() method
    try: 
        s3.upload_fileobj(photo_file, BUCKET, key)
        # generate a unique url for the img using the 3 var
        url = f"{S3_BASE_URL}{BUCKET}/{key}"
        Photo.objects.create(url=url, post_id=post_id)

    except Exception as error:
        # print err to debug
        print(f'Photo upload failed: {error}')
    # redirect to the detail pg
    return redirect('post_detail', post_id=post_id)


@login_required
# # AWS - Post Photo DELETE
def delete_photo(request, post_id, photo_id):
    # retrieve img
    post= get_object_or_404(Post, id=post_id)
    # photos = post.photo_set.all() # get the imgs related to this post
    photo = get_object_or_404(Photo, id=photo_id)

    # set up a s3 client obj for working with AMZN s3
    s3 = boto3.client('s3')

    # retrieve file name
    # for photo in photos:
    #     key = photo.url.split('/')[-1]

    key = photo.url.split('/')[-1]

    # delete img from AWS S3
    try:
        s3.delete_object(Bucket=BUCKET, Key=key)
    except Exception as error:
        print(f'Photo delete failed:{error}')

    post_id = post.id

    # delete from my db
    photo.delete()

    return redirect('post_detail', post_id=post_id)


# Comments
class AddComment(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ('content',)
    template_name = 'posts/comment_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.post_id = self.kwargs['post_id']
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        post.increment_comment_num()

        return super().form_valid(form)
    
    def get_success_url(self):
        post_id = self.kwargs['post_id']
        return reverse('post_detail', kwargs={'post_id': post_id})

class DeleteComment(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'posts/comment_confirm_delete.html'

    # override the get_success_url() method to dynamically retrieve the success URL 
    # based on the Comment model's get_absolute_url() method which includes the necessary URL param
    def get_success_url(self):
        post_id = self.kwargs['post_id']
        return reverse('post_detail', kwargs={'post_id': post_id})

    def form_valid(self, form):
        post_id = self.kwargs['post_id']
        post = get_object_or_404(Post, id=post_id)
        comment_id = self.kwargs['pk']
        comment = get_object_or_404(Comment, id=comment_id)

        post.decrement_comment_num()
        comment.delete()

        return super().form_valid(form)
    

# Likes
@login_required
def update_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user

    try:
        like = Like.objects.get(user=user, post=post)
        like.delete() # delete the obj from db
        post.decrement_like_num()
    except Like.DoesNotExist:
        Like.objects.create(user=user, post=post)
        post.increment_like_num()

    if 'HTTP_REFERER' in request.META:
        # Redirect the user back to the current pg
        return redirect(request.META['HTTP_REFERER'])
    else:
        return redirect('post_detail', post_id=post_id)


