import uuid
from django.db import models
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


# Modelo para los usuarios
class Usuario(AbstractUser):
    ROLES = [
        ('usuario', 'Usuario'),
        ('bibliotecario', 'Bibliotecario'),
        
    ]
    dni= models.CharField(max_length=9, unique=True)
    direccion= models.CharField(max_length=200, blank=True)
    telefono= models.CharField(max_length=15, blank=True)
    rol= models.CharField(max_length=20, choices=ROLES, default='usuario')
    
    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email
        super().save(*args, **kwargs)
    def __str__(self):
        return self.first_name + ' ' + self.last_name + ' (' + self.rol + ')' + ' - ' + self.email + ' - DNI: ' + self.dni
    
    
# Modelo para los libros
class Libro(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    titulo = models.CharField(max_length=200)
    autor = models.ManyToManyField('Autor', related_name='libros')
    editorial = models.CharField(max_length=100, blank=True)
    isbn = models.CharField(max_length=13, unique=True)
    copias = models.PositiveIntegerField(default=1)
    estado = models.CharField(max_length=50, default='disponible')
    def __str__(self):
        return self.titulo
    

# funcion para calcular la fecha de devolucion
def calcular_fecha_devolucion():
    return timezone.now().date() + timedelta(days=14)

# Modelo para los préstamos

class Prestamo(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    fecha_prestamo = models.DateField(auto_now_add=True)
    fecha_devolucion = models.DateField(default=calcular_fecha_devolucion)
    devuelto = models.BooleanField(default=False)

    def __str__(self):
        return f'Préstamo de {self.libro.titulo} a {self.usuario.first_name} desde {self.fecha_prestamo} hasta {self.fecha_devolucion}'
    
# Modelo para autores
class Autor(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    biografia = models.TextField(blank=True)

    def __str__(self):
        return self.nombre