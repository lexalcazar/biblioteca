# urls de la aplicacion prestamos
from django.urls import path    
from . import views
urlpatterns = [
    path('', views.index, name='index'),
]