## Context

El paquete `prestamos.api` ya publica la consulta anónima `GET /api/libros/` mediante Django REST Framework y mantiene separadas las vistas web. El modelo `Libro` tiene una relación muchos a muchos con `Autor`, y `Prestamo` conserva una referencia a cada libro. Esta ampliación debe preservar el contrato de lectura actual y añadir operaciones de escritura limitadas a la identidad autenticada de bibliotecarios. Véanse `proposal.md` y `specs/libros-api/spec.md`.

## Goals / Non-Goals

**Goals:**
- Añadir las rutas de colección y detalle necesarias para el CRUD de libros.
- Validar los datos de escritura y las referencias de autores antes de persistir cambios.
- Calcular el estado de disponibilidad a partir de las copias y rechazar la eliminación de libros con préstamos.
- Mantener sin autenticación las operaciones GET y sin cambios las rutas web legacy.

**Non-Goals:**
- Gestionar autores, préstamos o usuarios mediante nuevas rutas API.
- Permitir que el cliente asigne directamente el estado del libro.
- Implementar autenticación basada en datos enviados por el cliente o introducir roles nuevos.

## Decisions

### Vistas separadas para colección y detalle

Se ampliarán las vistas del paquete `prestamos.api` con una vista de colección para GET y POST, y una vista de detalle para GET, PUT, PATCH y DELETE. Ambas usarán consultas con autores precargados y el renderer JSON existente.

Se descarta un router o viewset automático porque las dos vistas concretas permiten controlar explícitamente los métodos públicos, las respuestas y los permisos por operación.

### Serializadores de lectura y escritura

El serializador actual se mantendrá para las respuestas, con autores anidados. Un serializador de escritura aceptará `autores_ids` como lista no vacía de claves de autores, expondrá los campos editables y tratará `estado` como solo lectura. Su validación calculará `estado` desde `copias` antes de crear o actualizar.

Se descarta aceptar autores anidados o permitir escribir `estado`, ya que ambos formatos ampliarían el contrato y permitirían incoherencias entre copias y disponibilidad.

### Permisos basados en el usuario autenticado

GET permanecerá disponible sin autenticación.

POST, PUT, PATCH y DELETE usarán un permiso DRF personalizado que permita únicamente usuarios autenticados cuyo atributo `rol` sea `bibliotecario`.

La autorización se realizará sobre `request.user` después de la autenticación y no se leerán DNI, roles ni otros datos enviados por el cliente para decidir los permisos.

Se descarta basar la autorización en campos de la solicitud porque esos valores no demuestran la identidad del solicitante.

### Autenticación de la API

Las operaciones protegidas utilizarán `BasicAuthentication` de Django REST Framework para identificar al usuario mediante las credenciales del modelo `Usuario` existente.

Después de autenticar al usuario, el permiso de la API comprobará que `request.user` esté autenticado y que su atributo `rol` sea `bibliotecario`.

Las operaciones GET continuarán siendo públicas.

No se añadirá en este cambio un sistema de tokens, JWT ni un endpoint específico de autenticación. En entornos distintos de desarrollo, la autenticación básica SHALL utilizarse únicamente sobre HTTPS.

### Eliminación protegida por préstamos

Antes de borrar un libro, la vista comprobará la existencia de préstamos asociados. Si los hay, responderá HTTP 409 sin alterar el libro ni los préstamos; de lo contrario, eliminará el libro y devolverá 204.

Se descarta confiar únicamente en el borrado en cascada del modelo porque eliminaría préstamos históricos y violaría el contrato de conservación.

## Risks / Trade-offs

- [El campo `estado` puede ser modificado fuera de la API] → Las escrituras API lo recalculan siempre a partir de `copias`; la consistencia de otros canales queda fuera de este cambio.
- [Los préstamos existentes bloquean eliminaciones] → La respuesta 409 comunica el conflicto sin pérdida de datos.
- [Más métodos aumentan la superficie de autorización] → Las pruebas cubrirán bibliotecario, usuario ordinario y cliente anónimo para cada categoría de escritura.

## Migration Plan

1. Añadir permisos, serializador de escritura, vistas y rutas de detalle dentro de `prestamos.api`.
2. Ampliar las pruebas de contrato CRUD, validación, permisos y protección de préstamos.
3. Ejecutar la suite Django sin migraciones de esquema.
4. Si se requiere reversión, eliminar las rutas y vistas de escritura; la ruta de consulta y las rutas web continúan intactas.
