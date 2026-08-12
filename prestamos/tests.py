from django.test import TestCase

from prestamos.models import Autor, Libro


class ListaLibrosApiTests(TestCase):
    def test_devuelve_libros_y_autores_en_json(self):
        autor = Autor.objects.create(nombre='Ursula', apellidos='Le Guin')
        libro = Libro.objects.create(
            titulo='Los desposeidos',
            editorial='Minotauro',
            isbn='9788445076461',
            copias=3,
            estado='disponible',
        )
        libro.autor.add(autor)

        respuesta = self.client.get('/api/libros/')

        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta['Content-Type'], 'application/json')
        self.assertEqual(
            respuesta.json(),
            [
                {
                    'id': str(libro.id),
                    'titulo': 'Los desposeidos',
                    'editorial': 'Minotauro',
                    'isbn': '9788445076461',
                    'copias': 3,
                    'estado': 'disponible',
                    'autores': [
                        {
                            'id': str(autor.id),
                            'nombre': 'Ursula',
                            'apellidos': 'Le Guin',
                        }
                    ],
                }
            ],
        )

    def test_devuelve_lista_vacia_si_no_hay_libros(self):
        respuesta = self.client.get('/api/libros/')

        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.json(), [])

    def test_rechaza_metodos_distintos_de_get(self):
        for method in ('post', 'put', 'patch', 'delete', 'head', 'options'):
            with self.subTest(method=method):
                respuesta = getattr(self.client, method)('/api/libros/')

                self.assertEqual(respuesta.status_code, 405)

    def test_ruta_web_de_libros_sigue_disponible(self):
        respuesta = self.client.get('/prestamos/libros/')

        self.assertEqual(respuesta.status_code, 200)
