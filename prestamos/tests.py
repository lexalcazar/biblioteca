import base64

from django.test import TestCase

from prestamos.models import Autor, Libro, Prestamo, Usuario


class ListaLibrosApiTests(TestCase):
    def setUp(self):
        self.autor = Autor.objects.create(nombre='Ursula', apellidos='Le Guin')
        self.bibliotecario = Usuario.objects.create_user(
            username='bibliotecario',
            password='secreto',
            dni='12345678A',
            rol='bibliotecario',
        )
        self.usuario = Usuario.objects.create_user(
            username='usuario', password='secreto', dni='87654321B', rol='usuario',
        )

    def autenticar_como(self, usuario):
        credenciales = base64.b64encode(
            f'{usuario.username}:secreto'.encode(),
        ).decode()
        self.client.defaults['HTTP_AUTHORIZATION'] = f'Basic {credenciales}'

    def crear_libro(self, **campos):
        campos.setdefault('titulo', 'Los desposeidos')
        campos.setdefault('isbn', '9788445076461')
        libro = Libro.objects.create(**campos)
        libro.autor.add(self.autor)
        return libro

    def test_devuelve_libros_y_autores_en_json(self):
        libro = self.crear_libro(editorial='Minotauro', copias=3, estado='disponible')

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
                            'id': str(self.autor.id),
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
        for method in ('head', 'options'):
            with self.subTest(method=method):
                respuesta = getattr(self.client, method)('/api/libros/')

                self.assertEqual(respuesta.status_code, 405)

    def test_ruta_web_de_libros_sigue_disponible(self):
        respuesta = self.client.get('/prestamos/libros/')

        self.assertEqual(respuesta.status_code, 200)

    def test_bibliotecario_puede_crear_libro(self):
        self.autenticar_como(self.bibliotecario)

        respuesta = self.client.post('/api/libros/', {
            'titulo': 'La mano izquierda de la oscuridad',
            'isbn': '9788445076478',
            'autores_ids': [str(self.autor.id)],
            'copias': 0,
            'estado': 'disponible',
        }, content_type='application/json')

        self.assertEqual(respuesta.status_code, 201)
        self.assertEqual(respuesta.json()['estado'], 'no disponible')
        self.assertEqual(respuesta.json()['autores'][0]['id'], str(self.autor.id))

    def test_creacion_invalida_no_persiste_libro(self):
        self.autenticar_como(self.bibliotecario)

        respuesta = self.client.post('/api/libros/', {
            'titulo': 'Invalido', 'isbn': '9788445076485', 'autores_ids': [],
        }, content_type='application/json')

        self.assertEqual(respuesta.status_code, 400)
        self.assertFalse(Libro.objects.filter(isbn='9788445076485').exists())

    def test_creacion_rechaza_isbn_duplicado_y_autor_inexistente(self):
        self.crear_libro()
        self.autenticar_como(self.bibliotecario)

        respuesta = self.client.post('/api/libros/', {
            'titulo': 'Duplicado',
            'isbn': '9788445076461',
            'autores_ids': [str(self.autor.id)],
        }, content_type='application/json')
        self.assertEqual(respuesta.status_code, 400)

        respuesta = self.client.post('/api/libros/', {
            'titulo': 'Autor invalido',
            'isbn': '9788445076485',
            'autores_ids': ['00000000-0000-0000-0000-000000000000'],
        }, content_type='application/json')
        self.assertEqual(respuesta.status_code, 400)

    def test_consulta_detalle_y_actualizaciones(self):
        libro = self.crear_libro(copias=1)

        respuesta = self.client.get(f'/api/libros/{libro.id}/')
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.json()['id'], str(libro.id))

        self.autenticar_como(self.bibliotecario)
        respuesta = self.client.put(f'/api/libros/{libro.id}/', {
            'titulo': 'Titulo reemplazado',
            'isbn': '9788445076492',
            'editorial': 'Minotauro',
            'copias': 2,
            'autores_ids': [str(self.autor.id)],
        }, content_type='application/json')
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.json()['titulo'], 'Titulo reemplazado')

        respuesta = self.client.patch(f'/api/libros/{libro.id}/', {
            'copias': 0,
        }, content_type='application/json')
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.json()['estado'], 'no disponible')

    def test_detalle_inexistente_devuelve_404(self):
        self.assertEqual(
            self.client.get('/api/libros/00000000-0000-0000-0000-000000000000/').status_code,
            404,
        )

    def test_actualizaciones_invalidas_e_inexistentes(self):
        libro = self.crear_libro()
        self.autenticar_como(self.bibliotecario)

        respuesta = self.client.put(f'/api/libros/{libro.id}/', {
            'titulo': 'Sin autores',
            'isbn': '9788445076522',
            'autores_ids': [],
        }, content_type='application/json')
        self.assertEqual(respuesta.status_code, 400)

        respuesta = self.client.patch(f'/api/libros/{libro.id}/', {
            'copias': -1,
        }, content_type='application/json')
        self.assertEqual(respuesta.status_code, 400)

        respuesta = self.client.put('/api/libros/00000000-0000-0000-0000-000000000000/', {
            'titulo': 'Inexistente',
            'isbn': '9788445076539',
            'autores_ids': [str(self.autor.id)],
        }, content_type='application/json')
        self.assertEqual(respuesta.status_code, 404)

        respuesta = self.client.patch('/api/libros/00000000-0000-0000-0000-000000000000/', {
            'titulo': 'Inexistente',
        }, content_type='application/json')
        self.assertEqual(respuesta.status_code, 404)

    def test_escrituras_requieren_bibliotecario(self):
        payload = {
            'titulo': 'Nuevo libro',
            'isbn': '9788445076508',
            'autores_ids': [str(self.autor.id)],
        }
        self.assertEqual(
            self.client.post('/api/libros/', payload, content_type='application/json').status_code,
            401,
        )

        self.autenticar_como(self.usuario)
        self.assertEqual(
            self.client.post('/api/libros/', payload, content_type='application/json').status_code,
            403,
        )

        libro = self.crear_libro()
        self.assertEqual(
            self.client.patch(
                f'/api/libros/{libro.id}/', {'titulo': 'Sin permiso'},
                content_type='application/json',
            ).status_code,
            403,
        )

    def test_eliminacion_y_conflicto_por_prestamos(self):
        libro = self.crear_libro()
        self.autenticar_como(self.bibliotecario)

        respuesta = self.client.delete(f'/api/libros/{libro.id}/')
        self.assertEqual(respuesta.status_code, 204)
        self.assertFalse(Libro.objects.filter(id=libro.id).exists())

        libro = self.crear_libro(isbn='9788445076515')
        Prestamo.objects.create(usuario=self.usuario, libro=libro)
        respuesta = self.client.delete(f'/api/libros/{libro.id}/')
        self.assertEqual(respuesta.status_code, 409)
        self.assertTrue(Libro.objects.filter(id=libro.id).exists())

    def test_eliminacion_inexistente_devuelve_404(self):
        self.autenticar_como(self.bibliotecario)
        respuesta = self.client.delete('/api/libros/00000000-0000-0000-0000-000000000000/')

        self.assertEqual(respuesta.status_code, 404)
