from django.urls import path
from .views import MovieList # Ou o nome da sua view

urlpatterns = [
    path('movies/', MovieList.as_view(), name='movie-list'),
]