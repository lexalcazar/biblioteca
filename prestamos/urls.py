# urls de la aplicacion prestamos
from django.urls import path    
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('libros/', views.lista_libros, name='lista_libros'),
    #path('libros/<str:libro_titulo>/', views.detalle_libro, name='detalle_libro'),
]