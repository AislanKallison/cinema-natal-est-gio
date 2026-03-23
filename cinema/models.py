from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import uuid


class User(AbstractUser):
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    # Evita conflito com auth.User padrão (related_name customizados)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return self.email or self.username


class Movie(models.Model):
    title = models.CharField(max_length=255)
    genre = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)  # ← CORRIGIDO: agora opcional!
    # Adicione outros campos comuns se precisar (ex: duration, poster, release_date)
    # duration = models.PositiveIntegerField(null=True, blank=True, help_text="Duração em minutos")
    # poster_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title


class Showtime(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='showtimes')
    date_time = models.DateTimeField()
    room = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.movie.title} - {self.date_time.strftime('%d/%m/%Y %H:%M')} - {self.room}"


class Seat(models.Model):
    showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE, related_name='seats')
    row = models.CharField(max_length=5)
    number = models.PositiveIntegerField()
    status = models.CharField(max_length=20, default='available')  # available, reserved, sold
    reserved_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='reserved_seats')
    reserved_until = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('showtime', 'row', 'number')
        verbose_name = 'Assento'
        verbose_name_plural = 'Assentos'

    def __str__(self):
        return f"{self.row}{self.number} ({self.showtime})"


class Ticket(models.Model):
    code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets')
    showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE, related_name='tickets')
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE, related_name='tickets')
    purchased_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ingresso {self.code} - {self.user} - {self.seat}"