# Diagrama de Clases - Sistema de Inventario de Maquillaje

## Descripción del Sistema

Este sistema implementa un catálogo de productos de maquillaje con autenticación de usuarios y panel de administración. El diseño sigue principios de programación orientada a objetos y patrones de diseño para la separación de responsabilidades.

## Clases del Sistema

### 1. **Modelos de Base de Datos (models.py)**

#### `Base`
- **Tipo**: Clase base de SQLAlchemy
- **Propósito**: Proporciona funcionalidad ORM común para todas las entidades

#### `Producto`
- **Atributos**:
  - `id: Integer` (PK)
  - `nombre: String`
  - `cantidad: Integer`
  - `descripcion: String`
  - `marca: String`
  - `categoria: String`
  - `imagen_url: String`
- **Responsabilidad**: Representar productos en la base de datos

#### `Usuario`
- **Atributos**:
  - `id: Integer` (PK)
  - `username: String` (unique)
  - `email: String` (unique)
  - `password: String` (hashed)
  - `is_admin: Boolean`
- **Responsabilidad**: Representar usuarios del sistema

### 2. **Esquemas de Validación (schemas.py)**

#### `ProductoBase`
- **Atributos**: Campos base del producto
- **Métodos**: Validación de datos de entrada

#### `ProductoCreate(ProductoBase)`
- **Responsabilidad**: Validar datos para crear productos

#### `Producto(ProductoBase)`
- **Responsabilidad**: Serializar productos para respuestas API

#### `UsuarioBase`
- **Atributos**: Campos base del usuario
- **Métodos**: Validación de datos de entrada

#### `UsuarioCreate(UsuarioBase)`
- **Responsabilidad**: Validar datos para crear usuarios

#### `UsuarioLogin`
- **Atributos**: `username`, `password`
- **Responsabilidad**: Validar credenciales de login

#### `Usuario(UsuarioBase)`
- **Responsabilidad**: Serializar usuarios para respuestas API

#### `Token`
- **Atributos**: `access_token`, `token_type`
- **Responsabilidad**: Representar tokens de autenticación

#### `LoginResponse`
- **Atributos**: `token`, `user`
- **Responsabilidad**: Respuesta completa de login

### 3. **Servicios de Autenticación (services/auth_service.py)**

#### `PasswordManager`
- **Métodos**:
  - `hash_password(password: str) -> str`
  - `verify_password(password: str, hashed: str) -> bool`
- **Responsabilidad**: Gestión segura de contraseñas
- **Patrón**: Utility Class

#### `TokenManager`
- **Atributos**:
  - `active_tokens: dict`
- **Métodos**:
  - `create_token(user_id, username, is_admin) -> str`
  - `validate_token(token: str) -> dict`
  - `invalidate_token(token: str)`
- **Responsabilidad**: Gestión de sesiones y tokens
- **Patrón**: Singleton (instancia global)

#### `AuthService`
- **Atributos**:
  - `password_manager: PasswordManager`
  - `token_manager: TokenManager`
- **Métodos**:
  - `authenticate_user(db, username, password) -> dict`
  - `create_session(user_data) -> str`
  - `verify_admin_access(token) -> bool`
  - `verify_user_access(token) -> dict`
  - `logout(token)`
- **Responsabilidad**: Orquestar proceso completo de autenticación
- **Patrón**: Facade Pattern

### 4. **Capa de Acceso a Datos (crud.py)**

#### Funciones CRUD para Productos:
- `crear_producto(db, producto)`
- `obtener_productos(db)`
- `actualizar_producto(db, id, datos)`
- `eliminar_producto(db, id)`

#### Funciones CRUD para Usuarios:
- `crear_usuario(db, usuario)`
- `obtener_usuario_por_username(db, username)`
- `obtener_usuario_por_email(db, email)`
- `obtener_usuarios(db)`

**Responsabilidad**: Abstraer operaciones de base de datos
**Patrón**: Repository Pattern

### 5. **Servicios de Negocio (services/)**

#### `ProductoService` 
- **Atributos**:
  - `db: Session` (inyección de dependencia)
- **Métodos**:
  - `crear_producto(data) -> Producto`
  - `obtener_productos() -> List[Producto]`
  - `obtener_producto_por_id(id) -> Producto`
  - `actualizar_producto(id, data) -> Producto`
  - `eliminar_producto(id) -> dict`
  - `buscar_productos_por_categoria(categoria) -> List[Producto]`
  - `buscar_productos_por_marca(marca) -> List[Producto]`
  - `verificar_stock_bajo(limite) -> List[Producto]`
- **Responsabilidad**: Lógica de negocio específica de productos
- **Patrón**: Repository Pattern con Service Layer

#### `UsuarioService`
- **Atributos**:
  - `db: Session` (inyección de dependencia)
  - `password_manager: PasswordManager` (composición)
- **Métodos**:
  - `crear_usuario(data) -> Usuario`
  - `obtener_usuarios() -> List[Usuario]`
  - `obtener_usuario_por_id(id) -> Usuario`
  - `obtener_usuario_por_username(username) -> Usuario`
  - `obtener_usuario_por_email(email) -> Usuario`
  - `actualizar_usuario(id, data) -> Usuario`
  - `eliminar_usuario(id) -> dict`
  - `cambiar_password(id, password) -> Usuario`
  - `obtener_administradores() -> List[Usuario]`
  - `obtener_usuarios_regulares() -> List[Usuario]`
  - `validar_credenciales(username, password) -> Usuario`
- **Responsabilidad**: Lógica de negocio específica de usuarios
- **Patrón**: Repository Pattern con Service Layer

### 6. **Controladores API (main.py)**

#### Rutas de Productos:
- `GET /productos/` - Listar productos (público)
- `POST /productos/` - Crear producto (solo admin)
- `PUT /productos/{id}` - Actualizar producto (solo admin)
- `DELETE /productos/{id}` - Eliminar producto (solo admin)
- `GET /productos/categoria/{categoria}` - Buscar por categoría (público)
- `GET /productos/marca/{marca}` - Buscar por marca (público)
- `GET /productos/stock-bajo` - Productos con stock bajo (solo admin)

#### Rutas de Usuarios:
- `POST /auth/register` - Registrar usuario
- `POST /auth/login` - Iniciar sesión
- `POST /auth/logout` - Cerrar sesión
- `GET /auth/me` - Obtener usuario actual
- `GET /usuarios/` - Listar usuarios (solo admin)
- `GET /usuarios/administradores` - Listar administradores (solo admin)

#### Rutas de Interfaz:
- `GET /` - Catálogo público
- `GET /admin` - Panel administrador (protegido)
- `GET /login` - Página de login

**Responsabilidad**: Manejar peticiones HTTP y coordinar servicios
**Patrón**: MVC Controller

### 7. **Configuración de Base de Datos (database.py)**

#### `SessionLocal`
- **Responsabilidad**: Factory para sesiones de base de datos

#### `engine`
- **Responsabilidad**: Motor de conexión a la base de datos

## Relaciones entre Clases

```
AuthService
├── PasswordManager (composición)
└── TokenManager (composición)

ProductoService
├── Session (inyección de dependencia)
└── Producto (maneja entidades)

UsuarioService
├── Session (inyección de dependencia)
├── PasswordManager (composición)
└── Usuario (maneja entidades)

API Controllers
├── AuthService (dependencia)
├── ProductoService (dependencia)
├── UsuarioService (dependencia)
└── Database Session (inyección de dependencia)

Producto ←→ ProductoService ←→ API Controllers
Usuario ←→ UsuarioService ←→ API Controllers
```

## Patrones de Diseño Implementados

1. **Repository Pattern**: Services abstraen acceso a datos con métodos específicos
2. **Service Layer Pattern**: Capa de servicios encapsula lógica de negocio
3. **Facade Pattern**: AuthService simplifica autenticación compleja
4. **Dependency Injection**: FastAPI inyecta dependencias automáticamente
5. **MVC Pattern**: Separación clara entre Modelo, Vista y Controlador
6. **Factory Pattern**: SessionLocal crea sesiones de BD
7. **Strategy Pattern**: Diferentes estrategias de autenticación posibles
8. **Composition Pattern**: Services componen otros objetos especializados

## Principios SOLID Aplicados

- **SRP**: Cada clase tiene una responsabilidad específica
- **OCP**: Sistema extensible para nuevos tipos de autenticación
- **LSP**: Esquemas Pydantic son intercambiables
- **ISP**: Interfaces específicas para cada funcionalidad
- **DIP**: Dependencias inyectadas, no hardcodeadas

## Arquitectura del Sistema

```
Frontend (HTML/JS) 
    ↓
API Controllers (FastAPI)
    ↓
Services Layer (AuthService, ProductoService)
    ↓
Data Access Layer (CRUD Functions)
    ↓
Database Models (SQLAlchemy)
    ↓
Database (SQLite/PostgreSQL)
```

Este diseño proporciona un sistema escalable, mantenible y siguiendo buenas prácticas de ingeniería de software.
