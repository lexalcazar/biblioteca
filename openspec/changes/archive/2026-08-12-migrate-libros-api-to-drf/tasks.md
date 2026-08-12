## 1. Infraestructura API

- [x] 1.1 Añadir Django REST Framework a las dependencias y a la configuración del proyecto.
- [x] 1.2 Crear el paquete `prestamos/api/` con `__init__.py`, `serializers.py`, `views.py` y `urls.py`, separando la API REST de las vistas web legacy.
- [x] 1.3 Implementar una vista DRF de lista de libros con autores precargados, renderer JSON exclusivo, paginación deshabilitada y solo GET.

## 2. Enrutamiento y sustitución

- [x] 2.1 Registrar `prestamos.api.urls` bajo `/api/` para conservar `GET /api/libros/`.
- [x] 2.2 Eliminar la vista JSON manual de las vistas web legacy sin modificar sus rutas ni plantillas.

## 3. Compatibilidad y verificación

- [x] 3.1 Actualizar las pruebas para validar el estado 200 y la estructura JSON completa para catálogos con libros y vacíos.
- [x] 3.2 Añadir pruebas que comprueben 405 para POST, PUT, PATCH, DELETE, HEAD y OPTIONS en `/api/libros/`.
- [x] 3.3 Confirmar mediante pruebas que una ruta web existente permanece disponible y ejecutar la suite Django.
