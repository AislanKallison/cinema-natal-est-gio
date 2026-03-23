from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    # Admin do Django (ÚNICO LUGAR)
    path('admin/', admin.site.urls),

    # Documentação OpenAPI/Swagger
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    # Inclui as rotas do app cinema
    path('api/', include('cinema.urls')),

    # Redireciona a raiz para a documentação
    path('', RedirectView.as_view(url='/api/docs/', permanent=False)),
]