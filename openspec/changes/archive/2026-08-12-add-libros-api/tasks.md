## 1. API de libros

- [x] 1.1 Implementar en `prestamos` una vista de solo lectura que admita GET, obtenga los libros con sus autores precargados y devuelva la estructura JSON especificada.
- [x] 1.2 Registrar `GET /api/libros/` en el enrutador del proyecto sin modificar las rutas web incluidas bajo `/prestamos/`.

## 2. Pruebas

- [x] 2.1 Añadir pruebas del catálogo con registros que validen el estado 200 y todos los campos de libros y autores del JSON.
- [x] 2.2 Añadir pruebas para catálogo vacío y para el rechazo con 405 de métodos distintos de GET.
- [x] 2.3 Añadir una prueba de regresión para una ruta web existente y ejecutar la suite de pruebas Django.
