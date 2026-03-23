from rest_framework import generics
from .models import Movie
from .serializers import MovieSerializer

class MovieList(generics.ListAPIView):
    queryset = Movie.objects.all()  # Isso busca o Batman no banco!
    serializer_class = MovieSerializer