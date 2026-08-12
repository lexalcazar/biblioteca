## Why

La primera API de libros usa una vista JSON manual, lo que dificulta adoptar convenciones y herramientas de Django REST Framework en futuras APIs. Se necesita migrar su implementación interna sin romper a los consumidores ni la aplicación web existente.

## What Changes

- Reimplementar `GET /api/libros/` con Django REST Framework.
- Conservar la URL, el método GET, el estado HTTP 200 y la estructura JSON actuales.
- Separar los componentes de la API de las vistas web legacy.
- Añadir Django REST Framework como dependencia del proyecto.

## Capabilities

### New Capabilities

Ninguna.

### Modified Capabilities

Ninguna. El contrato de `libros-api` permanece sin cambios.

## Impact

- Se reorganizará la implementación API dentro de la aplicación Django y se actualizará su enrutamiento.
- Se incorporará Django REST Framework a las dependencias del proyecto.
- Las pruebas verificarán la compatibilidad del contrato y que las rutas web existentes no cambian.
