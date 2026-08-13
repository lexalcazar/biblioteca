## 1. Escritura y autorización

- [x] 1.1 Añadir un serializador de escritura de libros que acepte `autores_ids`, valide los campos editables y calcule `estado` a partir de `copias`.
- [x] 1.2 Añadir un permiso DRF que autorice escrituras únicamente al usuario autenticado con rol `bibliotecario`.

## 2. Rutas CRUD

- [x] 2.1 Ampliar la vista de colección para mantener GET público y crear libros mediante POST con autenticación básica y permiso de bibliotecario.
- [x] 2.2 Implementar la vista de detalle para GET público y PUT, PATCH y DELETE protegidos mediante autenticación básica y permiso de bibliotecario, incluyendo respuesta 409 cuando existan préstamos asociados.
- [x] 2.3 Registrar la ruta `/api/libros/{id}/` dentro de `prestamos.api.urls` sin modificar las rutas web legacy.

## 3. Pruebas y verificación

- [x] 3.1 Añadir pruebas de creación, consulta individual, PUT y PATCH que cubran respuestas correctas, campos obligatorios, ISBN duplicado, `autores_ids` vacío o inválido, actualización parcial y cálculo automático de `estado` a partir de `copias`.
- [x] 3.2 Añadir pruebas de autorización para bibliotecarios, usuarios sin permiso y clientes no autenticados en las operaciones de escritura.
- [x] 3.3 Añadir pruebas de eliminación correcta, libro inexistente y conflicto por préstamos asociados.
- [x] 3.4 Ejecutar la suite Django y verificar que GET de catálogo y las rutas web existentes mantienen su comportamiento.
- [x] 3.5 Añadir pruebas de PUT y PATCH con datos inválidos que verifiquen HTTP 400 y con un UUID inexistente que verifiquen HTTP 404.
