from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register, name='register'),
    path('feed/', views.all_posts, name='feed'),
    
    # API ROUTES
    path('posts', views.new_post, name='newpost'),
]
