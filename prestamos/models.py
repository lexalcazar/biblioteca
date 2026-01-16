import uuid
from django.db import models

# Create your models here.
# Modelo para los usuarios
class Usuario(models.Model):
    ROLES = [
        ('usuario', 'Usuario'),
        ('bibliotecario', 'Bibliotecario'),
        
    ]
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    dni=models.CharField(max_length=9, unique=True)
    direccion = models.CharField(max_length=255, blank=True)
    telefono = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return self.nombre
# Modelo para los libros
class Libro(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13, unique=True)
    copias = models.PositiveIntegerField(default=1)
    estado = models.CharField(max_length=50, default='disponible')
    def __str__(self):
        return self.titulo
# Modelo para los préstamos
class Prestamo(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    fecha_prestamo = models.DateField(auto_now_add=True)
    fecha_devolucion = models.DateField(null=True, blank=True)
    devuelto = models.BooleanField(default=False)

    def __str__(self):
        return f'Préstamo de {self.libro.titulo} a {self.usuario.nombre}'