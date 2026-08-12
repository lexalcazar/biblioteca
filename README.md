# 📚 Biblioteca Django – Gestión de préstamos

Aplicación web desarrollada con **Django** para la gestión interna de una biblioteca.  
Permite administrar el catálogo de libros y gestionar los préstamos de usuarios.

El proyecto está orientado al desarrollo backend, el modelado de datos y la implementación de lógica de negocio real utilizando el framework Django.

---

## 🚀 Tecnologías utilizadas

- Python
- Django
- SQLite / PostgreSQL
- HTML5
- CSS3
- Django ORM

---

## ⚙️ Funcionalidades

### Gestión de libros
- Alta y edición
- Control del número total de copias
- Visualización de disponibilidad

### Gestión de usuarios
- Creación y administración de usuarios 
- Gestión interna por parte del bibliotecario

### Gestión de préstamos
- Registro de préstamos de libros a usuarios
- Registro de devoluciones
- Control automático de disponibilidad
- Relación entre usuarios, libros y préstamos

---

## 📖 Lógica de negocio implementada

- No permite realizar préstamos si no hay copias disponibles
- Actualización automática del número de copias al prestar o devolver
- Control del estado del préstamo (activo / devuelto)
- Relaciones entre entidades mediante claves foráneas
- Gestión centralizada desde el panel de administración de Django

---

## 🗂️ Modelos principales

- **Libro**
- **Usuario**
- **Prestamo**
- **Autor**

Relaciones implementadas mediante el ORM de Django.

---

## 🎯 Objetivo del proyecto

Proyecto desarrollado para consolidar conocimientos en:

- Django y arquitectura MVT
- Modelado de bases de datos con ORM
- Relaciones entre entidades
- Implementación de lógica de negocio
- Desarrollo de aplicaciones web backend

---

## 📌 Estado del proyecto

Proyecto funcional y en evolución.
