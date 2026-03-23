from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework import status
from cinema.models import Movie, Showtime, Seat

User = get_user_model()


class CinepolisAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Cria usuário de teste
        self.user = User.objects.create_user(
            username='testuser',
            email='test@email.com',
            password='123456'
        )

        # Cria filme - versão mínima para evitar erro de campos obrigatórios
        # Se o seu modelo exigir mais campos, adicione aqui
        self.movie = Movie.objects.create(
            title='Duna 2 Teste'
            # Se genre for obrigatório: , genre='Ficção Científica'
            # Se description for obrigatório: , description='Descrição teste'
            # Se duration for obrigatório: , duration=166
        )

        # Cria sessão
        self.showtime = Showtime.objects.create(
            movie=self.movie,
            date_time=timezone.now() + timezone.timedelta(hours=3),
            room='Sala 1'
        )

        # Cria assento
        self.seat = Seat.objects.create(
            showtime=self.showtime,
            row='A',
            number=5,
            status='available'
        )

    # CASE 1 - Registration
    def test_register_user(self):
        response = self.client.post('/api/register/', {
            'username': 'novoaluno',
            'email': 'novo@test.com',
            'password': 'teste123'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # CASE 2 - List movies
    def test_list_movies(self):
        response = self.client.get('/api/movies/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # CASE 3 - List showtimes
    def test_list_showtimes(self):
        url = f'/api/movies/{self.movie.id}/showtimes/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # CASE 4 + 5 - Reserve seat
    def test_reserve_seat(self):
        self.client.force_authenticate(user=self.user)
        url = f'/api/showtimes/{self.showtime.id}/seats/{self.seat.id}/reserve/'
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.seat.refresh_from_db()
        self.assertEqual(self.seat.status, 'reserved')