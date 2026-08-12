## Context

La aplicación Django agrupa el modelo `Libro` y las vistas web en `prestamos`; el enrutador de proyecto solo publica actualmente el administrador y las rutas web bajo `/prestamos/`. La API debe estar disponible en la ruta raíz `/api/libros/` sin modificar dichas rutas. Véanse `proposal.md` y `specs/libros-api/spec.md` para la motivación y el contrato externo.

## Goals / Non-Goals

**Goals:**
- Publicar una respuesta JSON con los campos de cada libro y de sus autores asociados definidos por la especificación.
- Evitar consultas adicionales por cada libro al recuperar sus autores.
- Mantener aisladas las vistas y plantillas HTML existentes.

**Non-Goals:**
- Crear, modificar o eliminar libros mediante la API.
- Añadir autenticación, paginación, filtrado o versionado de API.
- Modificar el esquema de datos o introducir dependencias de terceros.

## Decisions

### Vista JSON basada en Django

La vista limitará explícitamente el método HTTP permitido a GET, de modo que otros métodos reciban una respuesta 405 Method Not Allowed.

La respuesta se emitirá con `JsonResponse` usando una lista como cuerpo raíz.

Esta alternativa mantiene la primera API pequeña y no añade dependencias ni una capa de serialización adicional. Se descarta introducir Django REST Framework porque la única operación de lectura no justifica su configuración y dependencia.

### Ruta API en el enrutador del proyecto

El proyecto registrará `/api/libros/` de forma independiente de la inclusión existente de `prestamos.urls` bajo `/prestamos/`. Así se entrega la URL pública requerida sin cambiar el prefijo ni las rutas de la interfaz web.

Se descarta colocar la ruta en el conjunto web incluido actual, ya que produciría `/prestamos/api/libros/`, una URL distinta del contrato.

### Carga eficiente de autores

La consulta de libros usará precarga de la relación de autores antes de generar el JSON. Esto obtiene el catálogo y sus autores sin una consulta por libro, preservando el formato requerido para cada elemento de `autores`.

Se descarta consultar autores durante la serialización de cada libro por el patrón N+1 que causaría en catálogos grandes.

### Pruebas de contrato HTTP

Las pruebas Django crearán libros y autores de prueba y verificarán el estado 200, el tipo de respuesta JSON y los campos serializados. Un caso independiente verificará que un catálogo vacío devuelve una lista vacía; también se comprobará una ruta web ya existente para detectar una regresión de enrutamiento.

## Risks / Trade-offs

- [El catálogo completo puede crecer y producir respuestas grandes] → Esta primera versión queda deliberadamente sin paginación; podrá añadirse como cambio posterior con un contrato explícito.
- [La serialización manual debe mantenerse al evolucionar el modelo] → Las pruebas de contrato cubren todos los campos expuestos y la vista limita el JSON a la estructura especificada.
- [Registrar una ruta raíz puede interferir con rutas futuras] → Se usa el prefijo reservado `/api/`, separado de `/prestamos/` y `/admin/`.

## Migration Plan

1. Implementar la vista, registrar la ruta y añadir las pruebas.
2. Ejecutar la suite de pruebas Django antes del despliegue.
3. Desplegar sin migraciones de base de datos ni cambios de configuración.
4. Si se requiere reversión, eliminar la ruta y la vista API; las rutas web y los datos existentes permanecen intactos.
