from time import timezone
from urllib import request
from django.shortcuts import  get_object_or_404, render

from prestamos.forms import  AutorForm, DevolucionForm, LibroForm, PrestamoForm, UsuarioForm
from prestamos.models import Autor, Libro, Prestamo, Usuario

# Create your views here.
#Pagina de inicio de la aplicacion de prestamos
def index(request):
    return render(request, 'prestamos/index.html')
# listado de libros disponibles
def lista_libros(request):
    autores = Autor.objects.all()
    libros = Libro.objects.all()
    return render(request, 'prestamos/lista_libros.html', {'libros': libros, 'autores': autores})
# detalle de un libro
def detalle_libro(request, libro_titulo):
    autor = Autor.objects.get(libros__titulo=libro_titulo)
    libro = Libro.objects.get(titulo=libro_titulo)
    return render(request, 'prestamos/detalle_libro.html', {'libro': libro, 'autor': autor})
# vista del formulario crear usuario
def crear_usuario(request):
    form = UsuarioForm()
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'prestamos/usuario_creado.html', {'usuario': form.instance})
    return render(request, 'prestamos/crear_usuario.html', {'form': form})
# vista para usuario creado
def usuario_creado(request, usuario):
    return render(request, 'prestamos/usuario_creado.html', {'usuario': usuario})
#listado de usuarios
def lista_usuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, 'prestamos/lista_usuarios.html', {'usuarios': usuarios})
# vista para el formulario de añadir libro
def añadir_libro(request):
    form = LibroForm()
    if request.method == 'POST':
        form = LibroForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'prestamos/libro_creado.html', {'libro': form.instance})
    return render(request, 'prestamos/anadir_libro.html', {'form': form})
# vista para libro creado
def libro_creado(request, libro):
    return render(request, 'prestamos/libro_creado.html', {'libro': libro})
# vista formulario crear autor
def crear_autor(request):
    form = AutorForm()
    if request.method == 'POST':
        form = AutorForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'prestamos/autor_creado.html', {'autor': form.instance})
    return render(request, 'prestamos/crear_autor.html', {'form': form})
# vista para autor creado
def autor_creado(request, autor):
    return render(request, 'prestamos/autor_creado.html', {'autor': autor})
# vista de autores
def lista_autores(request):
    autores = Autor.objects.all()
    return render(request, 'prestamos/lista_autores.html', {'autores': autores})
# detalle de un autor
def detalle_autor(request, autor_nombre):
    autor = Autor.objects.get(nombre=autor_nombre)
    libros = Libro.objects.filter(autor=autor)
    return render(request, 'prestamos/detalle_autor.html', {'autor': autor, 'libros': libros})
# vista para crear prestamos
def crear_prestamo(request):
    form = PrestamoForm()
    if request.method == 'POST':
        form = PrestamoForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'prestamos/prestamo_creado.html', {'prestamo': form.instance})
    return render(request, 'prestamos/crear_prestamo.html', {'form': form})
# vista para prestamo creado
def prestamo_creado(request, prestamo):
    return render(request, 'prestamos/prestamo_creado.html', {'prestamo': prestamo})
# listado de prestamos
def lista_prestamos(request):
    prestamos = Prestamo.objects.all()
    return render(request, 'prestamos/lista_prestamos.html', {'prestamos': prestamos})
#vista formulario devolver libro 
def devolver_libro(request, prestamo_id):
    prestamo = get_object_or_404(Prestamo, id=prestamo_id)

    if request.method == "POST":
        form = DevolucionForm(request.POST, instance=prestamo)
        if form.is_valid():
            prestamo = form.save()
            return render(request, "prestamos/libro_devuelto.html", {"prestamo": prestamo})
    else:
        form = DevolucionForm(instance=prestamo)

    return render(request, "prestamos/devolver_libro.html", {"form": form, "prestamo": prestamo})
# vista para libro devuelto
def libro_devuelto(request, prestamo):
    return render(request, 'prestamos/libro_devuelto.html', {'prestamo': prestamo})
