from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from prestamos.api.serializers import LibroSerializer
from prestamos.models import Libro


class ListaLibrosApiView(APIView):
    renderer_classes = [JSONRenderer]

    def get(self, request):
        libros = Libro.objects.prefetch_related('autor')
        return Response(LibroSerializer(libros, many=True).data)

    def head(self, request):
        return self.http_method_not_allowed(request)

    def options(self, request):
        return self.http_method_not_allowed(request)
