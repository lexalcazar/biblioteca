from django.urls import path

from prestamos.api.views import LibroDetalleApiView, LibrosApiView


urlpatterns = [
    path('libros/', LibrosApiView.as_view(), name='lista_libros_api'),
    path('libros/<uuid:libro_id>/', LibroDetalleApiView.as_view(), name='detalle_libro_api'),
]
