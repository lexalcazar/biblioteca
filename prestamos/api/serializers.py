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


class LibroEscrituraSerializer(serializers.ModelSerializer):
    autores_ids = serializers.PrimaryKeyRelatedField(
        source='autor', many=True, queryset=Autor.objects.all(), allow_empty=False,
    )
    estado = serializers.CharField(read_only=True)

    class Meta:
        model = Libro
        fields = ('titulo', 'editorial', 'isbn', 'copias', 'estado', 'autores_ids')

    def create(self, validated_data):
        autores = validated_data.pop('autor')
        copias = validated_data.get('copias', 1)
        libro = Libro.objects.create(
            **validated_data,
            estado='disponible' if copias > 0 else 'no disponible',
        )
        libro.autor.set(autores)
        return libro

    def update(self, instance, validated_data):
        autores = validated_data.pop('autor', None)
        for campo, valor in validated_data.items():
            setattr(instance, campo, valor)
        instance.estado = 'disponible' if instance.copias > 0 else 'no disponible'
        instance.save()
        if autores is not None:
            instance.autor.set(autores)
        return instance
