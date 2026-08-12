## Context

La API actual está implementada como una vista Django manual dentro de `prestamos/views.py` y se registra directamente en el enrutador del proyecto. La migración incorpora Django REST Framework y debe mantener el contrato documentado en `openspec/specs/libros-api/spec.md`, mientras las vistas HTML existentes permanecen en su módulo actual. Véase `proposal.md` para la motivación.

## Goals / Non-Goals

**Goals:**
- Separar serialización, vistas y rutas API de las vistas web legacy.
- Mantener el cuerpo JSON, el estado 200 y la restricción de solo GET del endpoint existente.
- Seguir precargando los autores al consultar libros.

**Non-Goals:**
- Cambiar el contrato público de `libros-api`.
- Introducir operaciones de escritura, autenticación, paginación o una nueva versión de la API.
- Migrar las vistas HTML a Django REST Framework.

## Decisions

### Módulos API dedicados

### Módulos API dedicados

Se creará un paquete dedicado `prestamos/api/` para aislar completamente la API REST de las vistas web legacy.

La estructura será:

- `prestamos/api/__init__.py`
- `prestamos/api/serializers.py`
- `prestamos/api/views.py`
- `prestamos/api/urls.py`

El enrutador del proyecto incluirá `prestamos.api.urls` bajo `/api/` para conservar `GET /api/libros/`.

Se descarta mantener archivos API directamente en la raíz de `prestamos`, como `api_views.py`, `api_serializers.py` o `api_urls.py`, porque una carpeta dedicada proporciona una separación más clara y facilita añadir futuros endpoints sin mezclar la API con la aplicación web legacy.

### Serialización explícita con DRF

Un serializador de libro declarará los campos públicos actuales y un serializador anidado de autor con `id`, `nombre` y `apellidos`. Los UUID se representarán como cadenas JSON por el comportamiento estándar del serializador DRF.

Se descarta devolver directamente modelos o un diccionario manual, porque perdería la separación y las convenciones de serialización aportadas por DRF.

Para preservar el contrato existente, la vista utilizará exclusivamente el renderer JSON, evitando que la negociación de contenido produzca representaciones HTML u otros formatos.

### Vista de lista de solo lectura

La nueva vista DRF atenderá exclusivamente solicitudes GET y consultará `Libro` con los autores precargados. La respuesta será una lista JSON con estado 200.

Para preservar exactamente el contrato existente, los métodos HTTP distintos de GET, incluidos POST, PUT, PATCH, DELETE, HEAD y OPTIONS, deberán responder con 405 Method Not Allowed.

Se descarta usar un viewset o router automático: una vista de lista concreta expresa mejor el único endpoint soportado y evita exponer rutas no previstas.

### Pruebas de compatibilidad

Las pruebas existentes del endpoint se adaptarán para confirmar que la respuesta DRF conserva exactamente el contrato actual, incluido catálogo vacío y 405 para métodos no GET. También se mantendrá una prueba de una ruta web para proteger el aislamiento de la interfaz legacy.

## Risks / Trade-offs

- [Diferencias de serialización entre Django y DRF] → Las pruebas afirman el cuerpo JSON completo y el tipo de respuesta para libros con autores.
- [Configuración incompleta de DRF] → La dependencia y la configuración necesaria se añadirán junto con la vista antes de ejecutar las pruebas.
- [Rutas API y web mezcladas durante la migración] → El enrutador del proyecto incluirá módulos de rutas distintos para `/api/` y `/prestamos/`.

## Migration Plan

1. Añadir Django REST Framework y crear los módulos API aislados.
2. Sustituir el registro de la vista manual por la inclusión de rutas API, conservando `/api/libros/`.
3. Eliminar la vista JSON manual de las vistas web y actualizar las pruebas de contrato.
4. Ejecutar la suite Django y revertir restaurando la ruta y vista manual si fuera necesario; no hay migraciones de datos.
