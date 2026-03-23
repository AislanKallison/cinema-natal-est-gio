from django.contrib import admin
from .models import Movie, Showtime, Seat, Ticket # Importando os nomes corretos do seu models.py

admin.site.register(Movie)
admin.site.register(Showtime) # Agora vai funcionar!
admin.site.register(Seat)
admin.site.register(Ticket) 
