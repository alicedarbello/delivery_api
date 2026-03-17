# 🚀 Delivery API - FastAPI + SQLite

Una API REST moderna para gestionar un servicio de delivery, construida con **FastAPI** y **SQLite**. La aplicación permite la autenticación de usuarios, la gestión de pedidos y el control administrativo completo.

## 📋 Características Principales

- ✅ **Autenticación segura** con JWT (JSON Web Tokens)
- 🔐 **Contraseñas encriptadas** con bcrypt
- 📦 **Gestión de pedidos** con items personalizables
- 👥 **Control de usuarios** con roles (admin/cliente)
- 📊 **Cálculo automático** de totales de pedidos
- 🗄️ **Base de datos SQLite** con SQLAlchemy ORM
- 📚 **Documentación automática** con Swagger/OpenAPI
- 🔄 **Refresh Tokens** para sesiones largas

## 🛠️ Stack Tecnológico

- **Framework**: FastAPI 0.129.0
- **ORM**: SQLAlchemy 2.0.46
- **Base de datos**: SQLite
- **Autenticación**: JWT con python-jose
- **Encriptación**: bcrypt
- **Validación**: Pydantic 2.12.5
- **Server**: Uvicorn 0.41.0
- **Variables de entorno**: python-dotenv

## 📦 Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

## 🚀 Instalación

### 1. Clonar el repositorio
```bash
git clone <url-del-repositorio>
cd delivery_api
```

### 2. Crear un entorno virtual
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno
Crea un archivo `.env` en la raíz del proyecto:

```env
SECRET_KEY=tu_clave_secreta_aqui_muy_segura
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=sqlite:///banco.db
```

⚠️ **Nota de seguridad**: La `SECRET_KEY` debe ser una cadena larga (>32 caracteres) y aleatoria en producción.

## ▶️ Ejecutar la Aplicación

### Desarrollo
```bash
uvicorn main:app --reload
```

La API estará disponible en `http://localhost:8000`

### Documentación interactiva
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Producción
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## 🔐 Seguridad

### Autenticación y Autorización
- Los endpoints de órdenes requieren autenticación JWT
- Los usuarios solo pueden acceder a sus propios pedidos
- Los administradores pueden ver y modificar todos los pedidos
- Las contraseñas se encriptan con bcrypt

### Roles y Permisos
- **Cliente**: Puede crear, ver y modificar sus propios pedidos
- **Administrador**: Acceso completo a todos los pedidos y usuarios

### Tokens JWT
- **Access Token**: Válido por 30 minutos (configurable en `.env`)
- **Refresh Token**: Válido por 7 días

## 🗄️ Migraciones de Base de Datos (Alembic)

Para crear nuevas migraciones después de cambios en los modelos:

```bash
# Crear una nueva migración automática
alembic revision --autogenerate -m "Descripción del cambio"

# Aplicar las migraciones
alembic upgrade head

```

## 📚 Variables de Entorno Disponibles

| Variable | Descripción | Ejemplo |
|----------|-------------|---------|
| `SECRET_KEY` | Clave para firmar JWT | `tu_clave_muy_segura` |
| `ALGORITHM` | Algoritmo de firma | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Minutos de validez del token | `30` |
| `DATABASE_URL` | URL de conexión a BD | `sqlite:///banco.db` |

---

## 📁 Estructura del Proyecto

```
delivery_api/
├── main.py                # Punto de entrada de la aplicación
├── models.py              # Modelos de base de datos (User, Order, Item)
├── schemas.py             # Esquemas de validación Pydantic
├── auth_routes.py         # Rutas de autenticación
├── order_routes.py        # Rutas de gestión de pedidos
├── dependencies.py        # Dependencias compartidas
├── requirements.txt       # Dependencias del proyecto
├── .env                   # Variables de entorno
├── alembic/               # Migraciones de base de datos
├── banco.db               # Base de datos SQLite
├── alembic.ini            # Configuración de Alembic
└── README.md              # Este archivo
```

## 🗄️ Modelos de Datos

### User (Usuario)
```python
- id (int): Identificador único
- name (str): Nombre del usuario
- email (str): Email único
- password (str): Contraseña encriptada
- active (bool): Estado del usuario
- admin (bool): Indica si es administrador
```

### Order (Pedido)
```python
- id (int): Identificador único
- user_id (int): ID del usuario propietario
- status (str): Estado (PENDING, CANCELED, COMPLETED)
- total_price (float): Precio total calculado
- items (List[Item]): Lista de items del pedido
```

### Item (Artículo)
```python
- id (int): Identificador único
- quantity (int): Cantidad
- size (str): Tamaño
- flavor (str): Sabor/descripción
- unit_price (float): Precio unitario
- order_id (int): ID del pedido
```

**Hecho con ❤️ usando FastAPI**
