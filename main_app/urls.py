from django.urls import path # define URL patterns for Django app
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/signup/', views.signup, name='signup'),
    path('chatter/compose', views.PostCompose.as_view(), name='post_compose'),
    path('chatter/', views.posts_index, name='posts_index'),
    path('chatter/<int:post_id>/', views.post_detail, name='post_detail'),
]