from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.exceptions import APIException

from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from prestamos.api.permissions import EsBibliotecarioParaEscritura
from prestamos.api.serializers import LibroEscrituraSerializer, LibroSerializer
from prestamos.models import Libro


class ConflictoDeLibro(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = 'No se puede eliminar un libro con prestamos asociados.'


class LibrosApiView(APIView):
    renderer_classes = [JSONRenderer]
    authentication_classes = [BasicAuthentication]
    permission_classes = [EsBibliotecarioParaEscritura]
    http_method_names = ['get', 'post']

    def get(self, request):
        libros = Libro.objects.prefetch_related('autor')
        return Response(LibroSerializer(libros, many=True).data)

    def post(self, request):
        serializer = LibroEscrituraSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        libro = serializer.save()
        return Response(LibroSerializer(libro).data, status=status.HTTP_201_CREATED)


class LibroDetalleApiView(APIView):
    renderer_classes = [JSONRenderer]
    authentication_classes = [BasicAuthentication]
    permission_classes = [EsBibliotecarioParaEscritura]
    http_method_names = ['get', 'put', 'patch', 'delete']

    def get_object(self, libro_id):
        return get_object_or_404(Libro.objects.prefetch_related('autor'), id=libro_id)

    def get(self, request, libro_id):
        return Response(LibroSerializer(self.get_object(libro_id)).data)

    def put(self, request, libro_id):
        libro = self.get_object(libro_id)
        serializer = LibroEscrituraSerializer(libro, data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(LibroSerializer(serializer.save()).data)

    def patch(self, request, libro_id):
        libro = self.get_object(libro_id)
        serializer = LibroEscrituraSerializer(libro, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        return Response(LibroSerializer(serializer.save()).data)

    def delete(self, request, libro_id):
        libro = self.get_object(libro_id)
        if libro.prestamo_set.exists():
            raise ConflictoDeLibro
        libro.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def options(self, request):
        return self.http_method_not_allowed(request)
