from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("wiki/<str:title>/edit", views.edit_entry, name="edit_entry"),
    path("search/", views.search, name="search"),
    path("create/", views.create, name="create"),
    path("random", views.random_page, name="random")
]