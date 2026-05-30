# AI-LOG.md

## Herramientas de IA utilizadas

- Claude.ai
- Modelo: Sonnet 4.6 Low

---

## Stack elegido

### Backend
- Django 5
- SQLite

### Frontend
- Django Templates
- Bootstrap 5

### Autenticación
- Sistema de autenticación nativo de Django
- Gestión de sesiones mediante cookies
- Recuperación y cambio de contraseña mediante SMTP Gmail

---

## Justificación del stack

Elegí Django porque es el framework con el que tengo mayor experiencia y me permite implementar rápidamente autenticación, sesiones persistentes, vistas protegidas y gestión de usuarios.

Decidí utilizar Django Templates y Bootstrap en lugar de separar frontend y backend para reducir la complejidad de la solución y maximizar el tiempo disponible durante la prueba.

SQLite fue seleccionado para evitar configuraciones adicionales y acelerar el desarrollo.

---

## Funcionalidades implementadas

### Autenticación

- Login mediante email y contraseña.
- Sesión persistente utilizando el sistema de autenticación de Django.
- Logout.
- Vistas protegidas mediante autenticación.
- Recuperación de contraseña por correo electrónico.
- Cambio de contraseña.

### Roles

Se implementaron dos roles:

- Administrador
- Analista

### Dashboard

- Dashboard protegido.
- Redirección según rol.
- Indicador de usuario autenticado.

### Gestión de usuarios

- Listado de usuarios.
- Búsqueda de usuarios.
- Consulta de datos desde base de datos.

---

## Prompts utilizados

### Prompt 1

Genera un sistema de autenticación utilizando Django Authentication Framework con login, logout y vistas protegidas.

#### Resultado

La IA generó una implementación utilizando authenticate(), login() y logout().

#### Ajustes realizados

Se adaptó la lógica para trabajar con los roles Administrador y Analista.

---

### Prompt 2

Genera un modelo de usuario personalizado en Django con roles Administrador y Analista.

#### Resultado

La IA propuso extender AbstractUser incorporando un campo de rol mediante choices.

#### Ajustes realizados

Se simplificó la estructura para ajustarse a los requerimientos de la prueba.

---

### Prompt 3

Configura recuperación de contraseña utilizando SMTP Gmail en Django.

#### Resultado

La IA generó la configuración SMTP y el flujo de recuperación de contraseña.

#### Ajustes realizados

Se adaptaron las variables de entorno para mantener las credenciales fuera del repositorio.

---

### Prompt 4

Genera una tabla de usuarios con búsqueda dinámica utilizando Django Templates y JavaScript.

#### Resultado

La IA generó una implementación base para filtrar usuarios.

#### Ajustes realizados

Se modificó la consulta para adaptarla al modelo de usuario implementado.

---

## Caso donde rechacé o modifiqué una sugerencia de la IA

La IA propuso utilizar JWT y una arquitectura separada entre frontend y backend.

Decidí utilizar el sistema de sesiones nativo de Django y Django Templates porque los requisitos funcionales podían cumplirse completamente con menor complejidad y en menos tiempo de desarrollo.

Esta decisión permitió concentrar el esfuerzo en los requisitos prioritarios definidos por la prueba.

---

## Estimación de contribución

- Código generado inicialmente por IA: 60%
- Código escrito o modificado manualmente: 40%

---

## Lo mejor que hizo la IA

Aceleró significativamente la generación de estructuras repetitivas como vistas, formularios, autenticación y configuración SMTP.

---

## Lo que hizo mal la IA

En algunas ocasiones propuso soluciones más complejas de lo necesario para una prueba limitada a dos horas, incluyendo arquitecturas desacopladas y mecanismos de autenticación avanzados que no aportaban valor adicional para los requisitos solicitados.

---

## Reflexión final

La IA permitió acelerar la construcción de funcionalidades base, pero todas las implementaciones fueron revisadas, adaptadas y validadas antes de incorporarse al proyecto. Las decisiones finales de arquitectura, autenticación y organización del código fueron tomadas considerando el tiempo disponible y los objetivos de la prueba técnica.
