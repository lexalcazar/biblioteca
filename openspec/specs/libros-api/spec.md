# libros-api Specification

## Purpose

Permitir a clientes programáticos consultar el catálogo de libros existente mediante una respuesta JSON legible y consistente.

## Requirements

### Requirement: Consulta del catálogo de libros

El sistema SHALL exponer `GET /api/libros/` y responder con estado HTTP 200 y un cuerpo JSON consistente en una lista con todos los libros registrados.

Cada libro SHALL incluir:

- `id`
- `titulo`
- `editorial`
- `isbn`
- `copias`
- `estado`
- `autores`

Cada elemento de `autores` SHALL incluir:

- `id`
- `nombre`
- `apellidos`

#### Scenario: Catálogo con libros registrados

- **WHEN** un cliente realiza una solicitud `GET` a `/api/libros/` y existen libros registrados
- **THEN** el sistema responde con estado HTTP 200 y una lista JSON que representa todos los libros y sus autores asociados

#### Scenario: Catálogo vacío

- **WHEN** un cliente realiza una solicitud `GET` a `/api/libros/` y no existen libros registrados
- **THEN** el sistema responde con estado HTTP 200 y una lista JSON vacía

### Requirement: Aislamiento de la interfaz web

La incorporación de la consulta API SHALL conservar el comportamiento de las rutas y vistas web existentes.

#### Scenario: Consulta de una ruta web existente

- **WHEN** un usuario accede a una ruta web existente después de incorporar la API
- **THEN** el sistema mantiene la respuesta y el comportamiento previos de esa ruta
