from django.urls import path # define URL patterns for Django app
from . import views

urlpatterns = {
    path('', views.home, name='home'),
}