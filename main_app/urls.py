from django.urls import path # define URL patterns for Django app
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/signup/', views.signup, name='signup'),
    path('search/', views.search, name='search'),
    path('search_form/', views.search_form, name='search_form'),
    #user
    path('userprofile/<int:user_id>/add_avatar/', views.add_avatar, name='add_avatar'),
    path('userprofile/<int:user_id>/delete_avatar/', views.delete_avatar, name='delete_avatar'),
    path('userprofile/<int:user_id>/', views.user_profile, name='user_profile'),
    path('userprofile/<int:pk>/edit/', views.UserProfileEdit.as_view(), name='user_profile_edit'),
    path('user/<int:user_id>/follow/', views.follow, name='follow'),
    # posts
    path('chatter/compose/', views.PostCompose.as_view(), name='post_compose'),
    path('chatter/<int:post_id>/add_photo', views.add_photo, name='add_photo'),
    path('chatter/<int:post_id>/delete_photo/<int:photo_id>/', views.delete_photo, name='delete_photo'),
    path('chatter/', views.posts_index, name='posts_index'),
    path('chatter/<int:post_id>/', views.post_detail, name='post_detail'),
    path('chatter/<int:pk>/edit/', views.PostEdit.as_view(), name='post_edit'),
    path('chatter/<int:pk>/delete/', views.PostDelete.as_view(), name='post_delete'),
    path('chatter/<int:post_id>/repost/', views.repost, name='repost'),
    # comments
    path('chatter/<int:post_id>/add_comment/', views.AddComment.as_view(), name='add_comment'),
    path('chatter/<int:post_id>/delete_comment/<int:pk>/', views.DeleteComment.as_view(), name='comment_delete'),
    # likes
    path('chatter/<int:post_id>/update_like/', views.update_like, name='update_like'),
]

