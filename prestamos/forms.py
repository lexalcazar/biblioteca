# Formularios

# Formulario para crear usuario
from django.utils import timezone
from django import forms
from .models import Usuario, Libro, Prestamo, Autor

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['password', 'email', 'first_name', 'last_name', 'dni', 'direccion', 'telefono', 'rol']
        widgets = {
            'password': forms.PasswordInput(),
            'dni': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'rol': forms.Select(attrs={'class': 'form-control'}),
        }
    # validacion dni
    def clean_dni(self):
        dni = self.cleaned_data.get('dni')
        if len(dni) != 9:
            raise forms.ValidationError('El DNI debe tener 9 caracteres.')
        return dni
    # hasear hash de la password al guardarlo y username=email
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.username = self.cleaned_data['email']  
        if commit:
            user.save()
        return user
# Formulario añadir libro
class LibroForm(forms.ModelForm):
    dni_bibliotecario = forms.CharField(max_length=9, required=True, help_text='Ingrese su DNI de bibliotecario para verificar permisos.')
    class Meta:
        model = Libro
        fields = ['titulo', 'autor', 'isbn', 'editorial', 'copias', 'estado']
    widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'autor': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'isbn': forms.TextInput(attrs={'class': 'form-control'}),
            'editorial': forms.TextInput(attrs={'class': 'form-control'}),
            'copias': forms.NumberInput(attrs={'class': 'form-control'}),
            'estado': forms.TextInput(attrs={'class': 'form-control'}),
        }
    # Comprobar que lo inserta un bibliotecario
    def clean_dni_bibliotecario(self):
        dni = self.cleaned_data.get('dni_bibliotecario')
        try:
            usuario = Usuario.objects.get(dni=dni)
            if usuario.rol != 'bibliotecario':
                raise forms.ValidationError('El usuario no es un bibliotecario.')
        except Usuario.DoesNotExist:
            raise forms.ValidationError('No existe un usuario con ese DNI.')
        return dni
# Formulario para añadir autores
class AutorForm(forms.ModelForm):
    class Meta:
        model = Autor
        fields = ['nombre', 'apellidos', 'biografia']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control'}),
            'biografia': forms.Textarea(attrs={'class': 'form-control'}),
        }
# Formulario para crear prestamos
class PrestamoForm(forms.ModelForm):
    bibliotecario= forms.CharField(max_length=9, required=True, help_text='Ingrese su DNI de bibliotecario para verificar permisos.')
    class Meta:
        model = Prestamo
        fields = ['usuario', 'libro']
        widgets = {
            'usuario': forms.Select(attrs={'class': 'form-control'}),
            'libro': forms.Select(attrs={'class': 'form-control'}),
        }
    # Comprobar que lo inserta un bibliotecario
    def clean_bibliotecario(self):
        dni = self.cleaned_data.get('bibliotecario')
        try:
            usuario = Usuario.objects.get(dni=dni)
            if usuario.rol != 'bibliotecario':
                raise forms.ValidationError('El usuario no es un bibliotecario.')
        except Usuario.DoesNotExist:
            raise forms.ValidationError('No existe un usuario con ese DNI.')
        return dni
     # Comprobar que hay copias disponibles del libro
    def clean_libro(self):
        libro = self.cleaned_data.get('libro')
        # si no hay copias disponibles, lanzar error y cambiar estado del libro a 'no disponible'
        if libro.copias <= 0:
            libro.estado = 'no disponible'
            libro.save()
            raise forms.ValidationError('No hay copias disponibles de este libro.')
        return libro
    # Al guardar el prestamo, restar una copia del libro
    def save(self, commit=True):
        prestamo = super().save(commit=False)
        libro = prestamo.libro
        libro.copias -= 1
        if commit:
            libro.save()
            prestamo.save()
        return prestamo
    

# Formulario devolucion de prestamos, y cambniarestdao del prestamo a devuelto y actualizar las copias dispononibles del libro
class DevolucionForm(forms.ModelForm):
    prestamo = forms.ModelChoiceField(queryset=Prestamo.objects.filter(devuelto=False), widget=forms.Select(attrs={'class': 'form-control'}))
    class Meta:
        model = Prestamo
        fields = ['prestamo']
    # Al guardar la devolucion, actualizar el prestamo y el libro
    def save(self, commit=True):
        prestamo = super().save(commit=False)
        libro = prestamo.libro
        libro.copias += 1
        prestamo.devuelto = True
        prestamo.fecha_devolucion = timezone.now().date()
        if commit:
            libro.save()
            prestamo.save()
        return prestamo
