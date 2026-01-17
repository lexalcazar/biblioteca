# urls de la aplicacion prestamos
from django.urls import path    
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('libros/', views.lista_libros, name='lista_libros'),
    path('libros/<str:libro_titulo>/', views.detalle_libro, name='detalle_libro'),
    #path('crear_usuario/', views.crear_usuario, name='crear_usuario'),
    path('crear_usuario/', views.crear_usuario, name='crear_usuario'),
    # el siguiente path es para ver la pagina de usuario creado
    path('usuario_creado/', views.usuario_creado, name='usuario_creado'),
    path('usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('anadir_libro/', views.añadir_libro, name='anadir_libro'),
    path('libro_creado/', views.libro_creado, name='libro_creado'),
    path('crear_autor/', views.crear_autor, name='crear_autor'),
    path('autor_creado/', views.autor_creado, name='autor_creado'),
   

]