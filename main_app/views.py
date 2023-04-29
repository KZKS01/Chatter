from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Post, Photo, User, UserProfile
from django.db.models import Q # search fn: allows for complex queries using logical operators like &, |, and ~ (not)
import boto3
import uuid

S3_BASE_URL = 'https://s3.us-east-2.amazonaws.com/'
BUCKET = 'k-chatter'

# Create your views here.

def home(request):
    posts = Post.objects.all() # to be used in the html
    return render(request, 'home.html', {
        'posts': posts,
})


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
            # redirect user to home pg
            return redirect('home')
        # if not valid: generate an err msg
        else: 
            error_message = 'Invalid sign up - please try again.'

    # GET req: sign up form
    form = UserCreationForm() # send an empty form to client
    return render(request, 'registration/signup.html', {
        'form': form, # passing form data
        'error': error_message
    })


def user_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user_profile = UserProfile.objects.get(user=user)
    return render(request, 'users/user_profile.html', {
        'user': user,
        'user_profile': user_profile,
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
        form.instance.user = self.request.user # associate the new post with the user that created it
        # calls the parent class method form_valid and returns its result
        # the parent method saves the form data to the db & redirects to the success URL specified in the view
        return super().form_valid(form)

class PostEdit(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ('content', )
    template_name = 'posts/post_form.html'

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
    return render(request, 'posts/post_detail.html', {
        'post': post,
        'user': user,
        'user_id': user_id,
        })


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
        messages.error(request, f'Photo upload failed: {error}')
    # redirect to the detail pg
    return redirect('post_detail', post_id=post_id)


# AWS - Avatar Upload
def add_avatar(request, user_id):
    avatar_file = request.FILES.get('avatar-file', None)

    if avatar_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + avatar_file.name[avatar_file.name.rfind('.'):]

    try:
        s3.upload_fileobj(avatar_file, BUCKET, key)
        url = f"{S3_BASE_URL}{BUCKET}/{key}"
        UserProfile.objects.create(url=url, user_id=user_id)

    except Exception as error:
        messages.error(request, f'Avatar upload failed: {error}')

    return redirect('user_profile', user_id=user_id)


@login_required
# # AWS - Photo DELETE
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