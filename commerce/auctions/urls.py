from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('add/', views.add_listing, name='add_listing'),
    path('categories/', views.categories, name='categories'),
    path('listing/<int:listing_id>/', views.listing_detail, name='listing_detail'),
    path('listing/<int:listing_id>/watchlist/', views.toogle_watchlist, name='toggle_watchlist'),
    path('watchlist/', views.display_watchlist, name='watchlist'),
    path('category/<str:category_name>/', views.category_listings, name='category_listings'),
]
