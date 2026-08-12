## Why

Los consumidores programáticos no pueden consultar el catálogo de libros sin usar la interfaz web. Se necesita una primera API HTTP que exponga el inventario existente en un formato interoperable sin alterar los flujos actuales de la aplicación.

## What Changes

- Añadir el endpoint `GET /api/libros/` que devuelva en JSON la lista de libros registrados.
- Reutilizar el modelo `Libro` actual como fuente de los datos de la respuesta.
- Mantener sin cambios el comportamiento y las rutas de la aplicación web existente.

## Capabilities

### New Capabilities
- `libros-api`: Consulta HTTP en JSON del catálogo de libros mediante `GET /api/libros/`.

### Modified Capabilities

Ninguna.

## Impact

- Se incorporará una ruta y vista API en el proyecto Django.
- La respuesta leerá registros del modelo `Libro` existente.
- Se añadirán pruebas para el endpoint.
- No se modificarán las vistas ni las rutas web existentes.