from rest_framework import serializers

from prestamos.models import Autor, Libro


class AutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Autor
        fields = ('id', 'nombre', 'apellidos')


class LibroSerializer(serializers.ModelSerializer):
    autores = AutorSerializer(source='autor', many=True, read_only=True)

    class Meta:
        model = Libro
        fields = ('id', 'titulo', 'editorial', 'isbn', 'copias', 'estado', 'autores')
