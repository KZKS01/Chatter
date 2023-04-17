from django.urls import path # define URL patterns for Django app
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/signup/', views.signup, name='signup'),
    # path('chatter/', views.posts_index, name='posts_index'),
]