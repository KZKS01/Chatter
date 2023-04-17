from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required

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

# @login_required
# def posts_index(request):
