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

### Requirement: Creación de libros

El sistema SHALL aceptar `POST /api/libros/` para usuarios autenticados con rol `bibliotecario`. La solicitud SHALL incluir `titulo`, `isbn` y una lista no vacía `autores_ids` de autores existentes; podrá incluir `editorial` y `copias`.

`copias` SHALL ser un entero igual o superior a cero y tendrá valor 1 cuando no sea enviado. `estado` SHALL ser de solo lectura y será `disponible` cuando `copias` sea mayor que cero o `no disponible` cuando sea cero. Con datos válidos, el sistema SHALL responder HTTP 201 con la representación JSON del libro.

#### Scenario: Creación correcta de un libro

- **WHEN** un bibliotecario autenticado envía un POST con campos requeridos, autores existentes y datos válidos
- **THEN** el sistema responde HTTP 201 y devuelve el libro creado con sus autores asociados

#### Scenario: Creación con datos inválidos

- **WHEN** un bibliotecario autenticado envía campos requeridos incompletos, ISBN duplicado, copias inválidas, autores vacíos o un autor inexistente
- **THEN** el sistema responde HTTP 400 y no crea un libro

### Requirement: Consulta individual de libros

El sistema SHALL exponer `GET /api/libros/{id}/` y responder HTTP 200 con la misma representación JSON de libro usada por el catálogo.

#### Scenario: Consulta de un libro existente

- **WHEN** un cliente realiza GET a `/api/libros/{id}/` con un ID existente
- **THEN** el sistema responde HTTP 200 con el libro y sus autores

#### Scenario: Consulta de un libro inexistente

- **WHEN** un cliente realiza GET a `/api/libros/{id}/` con un ID inexistente
- **THEN** el sistema responde HTTP 404

### Requirement: Actualización de libros

El sistema SHALL permitir a bibliotecarios autenticados actualizar libros con `PUT /api/libros/{id}/` y `PATCH /api/libros/{id}/`. PUT SHALL requerir `titulo`, `isbn` y `autores_ids`; PATCH SHALL permitir un subconjunto de los campos editables `titulo`, `isbn`, `editorial`, `copias` y `autores_ids`.

`estado` SHALL ser de solo lectura y SHALL recalcularse en función de `copias`. Con datos válidos, el sistema SHALL responder HTTP 200 con la representación actualizada.

#### Scenario: Reemplazo total correcto

- **WHEN** un bibliotecario autenticado realiza PUT con todos los campos obligatorios y datos válidos
- **THEN** el sistema responde HTTP 200 con los datos de reemplazo

#### Scenario: Actualización parcial correcta

- **WHEN** un bibliotecario autenticado realiza PATCH con campos editables válidos
- **THEN** el sistema responde HTTP 200 y conserva los campos no enviados

#### Scenario: Actualización de copias

- **WHEN** una actualización establece `copias` en cero o en un valor mayor que cero
- **THEN** el sistema establece `estado` en `no disponible` o `disponible`, respectivamente

#### Scenario: Actualización inválida o inexistente

- **WHEN** un bibliotecario actualiza datos inválidos o un ID inexistente
- **THEN** el sistema responde HTTP 400 o HTTP 404, respectivamente

### Requirement: Eliminación de libros

El sistema SHALL permitir DELETE de `/api/libros/{id}/` únicamente a bibliotecarios autenticados y únicamente si el libro no tiene préstamos asociados.

#### Scenario: Eliminación correcta de un libro sin préstamos

- **WHEN** un bibliotecario autenticado elimina un libro existente sin préstamos
- **THEN** el sistema responde HTTP 204 sin cuerpo y elimina el libro

#### Scenario: Eliminación de un libro con préstamos asociados

- **WHEN** un bibliotecario autenticado elimina un libro con préstamos asociados
- **THEN** el sistema responde HTTP 409 y conserva el libro y los préstamos

#### Scenario: Eliminación de un libro inexistente

- **WHEN** un bibliotecario autenticado elimina un ID inexistente
- **THEN** el sistema responde HTTP 404

### Requirement: Autorización de operaciones de escritura

El sistema SHALL permitir GET de libros sin autenticación. POST, PUT, PATCH y DELETE SHALL requerir un usuario autenticado con rol `bibliotecario`; la autorización SHALL usar exclusivamente la identidad del usuario autenticado y no datos del cliente como el DNI.

#### Scenario: Escritura realizada por un bibliotecario autenticado

- **WHEN** un bibliotecario autenticado realiza una operación de escritura válida
- **THEN** el sistema permite procesarla

#### Scenario: Escritura realizada por un usuario no autorizado

- **WHEN** un cliente no autenticado o un usuario sin rol bibliotecario intenta una operación de escritura
- **THEN** el sistema rechaza la operación
