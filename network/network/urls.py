from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register, name='register'),
    path('network/<str:user>/', views.profile_view, name='profile'),
    path('followings/', views.followed_posts, name='followed'),
    
    # API ROUTES
    path('posts', views.new_post, name='newpost'),
    path('follow', views.toggle_follow, name='follow'),
    path('follow_stats/<str:user>/', views.follow_stats, name='follow_stats'),
    path('post/<int:post_id>/edit/', views.edit_post, name='editpost'),
    path('post/<int:post_id>/like/', views.like_post, name='likepost')
]
