from django.shortcuts import render

# Create your views here.
#Pagina de inicio de la aplicacion de prestamos
def index(request):
    return render(request, 'prestamos/index.html')
# listado de libros disponibles
def lista_libros(request):
    return render(request, 'prestamos/lista_libros.html')
# detalle de un libro
def detalle_libro(request, libro_titulo):
    return render(request, 'prestamos/detalle_libro.html', {'libro_titulo': libro_titulo})