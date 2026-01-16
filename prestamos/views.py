from django.shortcuts import render

# Create your views here.
#Pagina de inicio de la aplicacion de prestamos
def index(request):
    return render(request, 'prestamos/index.html')