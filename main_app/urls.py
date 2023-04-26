from django.urls import path # define URL patterns for Django app
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/signup/', views.signup, name='signup'),
    # posts
    path('chatter/compose/', views.PostCompose.as_view(), name='post_compose'),
    path('chatter/<int:post_id>/add_photo', views.add_photo, name='add_photo'),
    path('chatter/<int:post_id>/delete_photo/<int:photo_id>/', views.delete_photo, name='delete_photo'),
    path('chatter/', views.posts_index, name='posts_index'),
    path('chatter/<int:post_id>/', views.post_detail, name='post_detail'),
    path('chatter/<int:pk>/edit/', views.PostEdit.as_view(), name='post_edit'),
    path('chatter/<int:pk>/delete/', views.PostDelete.as_view(), name='post_delete'),
    path('search/', views.search, name='search'),
    # user
    path('profile/', views.user_profile, name='user_profile'),
]


# TODO: DELETE FN; USER IMG; ADDS COMMENT FUNCTION