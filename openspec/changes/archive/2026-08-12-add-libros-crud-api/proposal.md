## Why

La API de libros solo permite consultar el catálogo, por lo que los clientes programáticos siguen dependiendo de formularios web para administrar libros. Ampliar la API permite integrar la gestión del catálogo desde otros consumidores sin alterar los flujos web actuales.

## What Changes

- Mantener `GET /api/libros/` como consulta pública del catálogo existente.
- Añadir consulta individual pública mediante `GET /api/libros/{id}/`.
- Añadir creación de libros mediante `POST /api/libros/`.
- Añadir reemplazo total mediante `PUT /api/libros/{id}/`.
- Añadir actualización parcial mediante `PATCH /api/libros/{id}/`.
- Añadir eliminación mediante `DELETE /api/libros/{id}/`.
- Restringir `POST`, `PUT`, `PATCH` y `DELETE` a usuarios autenticados con rol de bibliotecario.
- Validar mediante Django REST Framework los datos de los libros y las referencias a autores existentes.
- No utilizar datos proporcionados por el cliente, como el DNI, como mecanismo de autorización para las operaciones de la API.
- No añadir operaciones CRUD independientes para autores en este cambio.
- Mantener la API separada de las vistas web legacy y conservar las rutas y el comportamiento web existentes.

## Capabilities

### New Capabilities

Ninguna.

### Modified Capabilities

- `libros-api`: Amplía la API de libros con operaciones CRUD sin cambiar la consulta de catálogo existente ni la interfaz web.

## Impact

- Se ampliarán los serializadores, vistas y rutas del paquete `prestamos.api`.
- Se reutilizará el modelo `Libro` y la relación existente con `Autor`.
- Se incorporará autenticación y autorización para restringir las operaciones que modifican libros a usuarios con rol de bibliotecario.
- Se añadirán pruebas de creación, consulta individual, actualización y eliminación, además de pruebas de permisos y compatibilidad con el comportamiento existente.
- Las vistas y rutas web legacy permanecerán sin cambios.
