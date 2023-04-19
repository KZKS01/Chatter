from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from .models import Post


# Create your views here.
def home(request):
    return render(request, 'home.html')

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


@login_required
def posts_index(request):
    posts = Post.objects.filter(user=request.user) # to be used in the html
    username = request.user.username
    user_id = request.user.id
    return render(request, 'posts/posts_index.html', {
        'posts': posts, 
        'username' : username,
        'user_id': user_id,
        })

@login_required
def post_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    user = request.user
    return render(request, 'posts/post_detail.html', {
        'post': post,
        'user': user,
        })