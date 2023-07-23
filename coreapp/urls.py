from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('myposts/', views.myposts, name='myposts'),
    path('myfeed/', views.myfeed, name='myfeed'),
    path('profile/', views.profile, name='profile')
    # Add more URL patterns for your views
]
