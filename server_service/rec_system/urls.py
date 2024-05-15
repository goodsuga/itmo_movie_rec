from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("view_all_movies/", views.view_all_movies, name="view_all_movies")
]