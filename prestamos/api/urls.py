from django.urls import path

from prestamos.api.views import ListaLibrosApiView


urlpatterns = [
    path('libros/', ListaLibrosApiView.as_view(), name='lista_libros_api'),
]
