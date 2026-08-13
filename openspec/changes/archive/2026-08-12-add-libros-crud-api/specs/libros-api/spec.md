## ADDED Requirements

### Requirement: Creación de libros

El sistema SHALL aceptar `POST /api/libros/` para usuarios autenticados con rol `bibliotecario`.

La solicitud SHALL incluir `titulo`, `isbn` y `autores_ids`, siendo `autores_ids` una lista no vacía de identificadores de autores existentes. Podrá incluir opcionalmente `editorial` y `copias`.

El campo `copias` SHALL ser un número entero igual o superior a cero y tendrá valor 1 cuando no sea enviado.

El campo `estado` SHALL ser de solo lectura en la API y será determinado por el sistema: `disponible` cuando `copias` sea mayor que cero y `no disponible` cuando `copias` sea cero.

Cuando los datos sean válidos, el sistema SHALL crear el libro y responder con estado HTTP 201 y su representación JSON.

#### Scenario: Creación correcta de un libro

- **WHEN** un bibliotecario autenticado envía un POST con los campos requeridos, autores existentes y datos válidos
- **THEN** el sistema responde con estado HTTP 201 y devuelve el libro creado con sus autores asociados

#### Scenario: Creación con datos inválidos

- **WHEN** un bibliotecario autenticado envía un POST sin campos requeridos, con ISBN duplicado, `copias` inválidas, una lista de autores vacía o un identificador de autor inexistente
- **THEN** el sistema responde con estado HTTP 400 y no crea el libro

### Requirement: Consulta individual de libros
El sistema SHALL exponer `GET /api/libros/{id}/` y responder con estado HTTP 200 y la misma representación JSON de libro usada por el catálogo.

#### Scenario: Consulta de un libro existente
- **WHEN** un cliente realiza GET a `/api/libros/{id}/` con el ID de un libro existente
- **THEN** el sistema responde con estado HTTP 200 y el libro solicitado con sus autores

#### Scenario: Consulta de un libro inexistente
- **WHEN** un cliente realiza GET a `/api/libros/{id}/` con un ID que no corresponde a un libro
- **THEN** el sistema responde con estado HTTP 404

### Requirement: Actualización de libros

El sistema SHALL permitir a usuarios autenticados con rol `bibliotecario` actualizar libros existentes mediante `PUT /api/libros/{id}/` y `PATCH /api/libros/{id}/`.

`PUT` SHALL requerir una representación completa de los campos editables obligatorios del libro, incluyendo `titulo`, `isbn` y `autores_ids`.

`PATCH` SHALL permitir actualizar únicamente los campos editables enviados.

Los campos editables SHALL ser `titulo`, `isbn`, `editorial`, `copias` y `autores_ids`.

El campo `estado` SHALL ser de solo lectura y SHALL actualizarse automáticamente en función de `copias`.

Cuando la solicitud sea válida, el sistema SHALL responder con estado HTTP 200 y la representación JSON actualizada del libro.

#### Scenario: Reemplazo total correcto

- **WHEN** un bibliotecario autenticado realiza PUT sobre un libro existente con todos los campos obligatorios, autores válidos y datos válidos
- **THEN** el sistema responde con estado HTTP 200 y devuelve el libro con los datos de reemplazo

#### Scenario: Actualización parcial correcta

- **WHEN** un bibliotecario autenticado realiza PATCH sobre un libro existente con un subconjunto válido de campos editables
- **THEN** el sistema responde con estado HTTP 200 y conserva los campos editables que no fueron enviados

#### Scenario: Actualización de copias

- **WHEN** una actualización establece `copias` en cero
- **THEN** el sistema establece `estado` en `no disponible`

#### Scenario: Actualización con copias disponibles

- **WHEN** una actualización establece `copias` en un valor mayor que cero
- **THEN** el sistema establece `estado` en `disponible`

#### Scenario: Actualización inválida o inexistente

- **WHEN** un bibliotecario actualiza un libro con datos inválidos o utiliza un ID inexistente
- **THEN** el sistema responde con estado HTTP 400 para datos inválidos o HTTP 404 para un libro inexistente

### Requirement: Eliminación de libros

El sistema SHALL permitir `DELETE /api/libros/{id}/` únicamente a usuarios autenticados con rol `bibliotecario`.

El sistema SHALL permitir eliminar un libro únicamente cuando no tenga préstamos asociados.

#### Scenario: Eliminación correcta de un libro sin préstamos

- **WHEN** un bibliotecario autenticado realiza DELETE sobre un libro existente que no tiene préstamos asociados
- **THEN** el sistema elimina el libro y responde con estado HTTP 204 sin cuerpo

#### Scenario: Eliminación de un libro con préstamos asociados

- **WHEN** un bibliotecario autenticado realiza DELETE sobre un libro que tiene uno o más préstamos asociados
- **THEN** el sistema responde con estado HTTP 409 y conserva tanto el libro como sus préstamos

#### Scenario: Eliminación de un libro inexistente

- **WHEN** un bibliotecario autenticado realiza DELETE sobre un ID que no corresponde a ningún libro
- **THEN** el sistema responde con estado HTTP 404

### Requirement: Autorización de operaciones de escritura

El sistema SHALL permitir las operaciones GET de libros sin requerir autenticación.

Las operaciones POST, PUT, PATCH y DELETE SHALL requerir que el usuario esté autenticado y tenga el rol `bibliotecario`.

La autorización SHALL basarse exclusivamente en la identidad del usuario autenticado y no en datos proporcionados por el cliente, como el DNI.

#### Scenario: Escritura realizada por un bibliotecario autenticado

- **WHEN** un usuario autenticado con rol `bibliotecario` realiza una operación POST, PUT, PATCH o DELETE válida
- **THEN** el sistema permite procesar la operación

#### Scenario: Escritura realizada por un usuario no autenticado

- **WHEN** un cliente no autenticado intenta realizar POST, PUT, PATCH o DELETE
- **THEN** el sistema rechaza la operación

#### Scenario: Escritura realizada por un usuario sin rol de bibliotecario

- **WHEN** un usuario autenticado cuyo rol no es `bibliotecario` intenta realizar POST, PUT, PATCH o DELETE
- **THEN** el sistema rechaza la operación por falta de permisos
