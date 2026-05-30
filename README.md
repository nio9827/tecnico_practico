# DevPanel

Mini panel administrativo desarrollado con Django, Templates y Bootstrap.

## Requisitos

* Python 3.11 o superior
* Git

---

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/usuario/devpanel-tu-nombre.git
cd devpanel-tu-nombre
```

### 2. Crear entorno virtual

Windows

```bash
python -m venv venv
venv\Scripts\activate
```

Linux / Mac

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## Configuración de Base de Datos

Ejecutar migraciones:

```bash
python manage.py migrate
```

---

## Crear Superusuario

Ejecutar:

```bash
python manage.py createsuperuser
```

Completar los datos solicitados:

```text
Username:
Email:
Password:
```

---

## Ejecutar el Proyecto

Iniciar servidor de desarrollo:

```bash
python manage.py runserver
```

Por defecto estará disponible en:

```text
http://127.0.0.1:8000/
```

---

## Acceso al Sistema

### Login

Ingresar desde:

```text
http://127.0.0.1:8000/
```

o la ruta configurada para login.

---

### Panel Administrativo Django

Ingresar desde:

```text
http://127.0.0.1:8000/admin/
```

Utilizar las credenciales creadas con:

```bash
python manage.py createsuperuser
```

---

## Credenciales de Prueba

Administrador

```text
Email: admin@test.com
Contraseña: admin123
```

Analista

```text
Email: analista@test.com
Contraseña: analista123
```

*(Modificar según los usuarios creados durante la carga inicial de datos.)*

---

## Funcionalidades

* Login con autenticación Django
* Roles Administrador y Analista
* Dashboard protegido
* Gestión de usuarios
* Búsqueda de usuarios
* Cambio de contraseña
* Panel administrativo Django

---
