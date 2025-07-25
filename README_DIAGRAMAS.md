# 📊 Diagramas UML del Sistema

Este proyecto incluye varios diagramas UML creados con PlantUML para documentar la arquitectura y funcionamiento del sistema.

## 📋 Archivos de Diagramas

### 1. **`diagrama_clases.puml`** - Diagrama de Clases Principal
- **Descripción**: Muestra todas las clases del sistema, sus atributos, métodos y relaciones
- **Incluye**: 
  - Modelos de base de datos (SQLAlchemy)
  - Esquemas de validación (Pydantic)
  - Servicios de negocio (Repository Pattern)
  - Controladores API
  - Patrones de diseño aplicados

### 2. **`arquitectura_sistema.puml`** - Arquitectura por Capas
- **Descripción**: Vista de alto nivel de la arquitectura del sistema
- **Muestra**: Separación en capas (Presentación, Lógica de Negocio, Acceso a Datos)

### 3. **`secuencia_login.puml`** - Diagrama de Secuencia: Login
- **Descripción**: Flujo completo del proceso de autenticación de usuario administrador
- **Actores**: Usuario, Frontend, API, Servicios, Base de Datos

### 4. **`secuencia_crear_producto.puml`** - Diagrama de Secuencia: Crear Producto
- **Descripción**: Flujo del proceso de creación de productos (solo administradores)
- **Incluye**: Verificación de permisos y operaciones CRUD

## 🔧 Cómo Visualizar los Diagramas

### Opción 1: PlantUML Online (Recomendado)
1. Ve a [PlantUML Online Server](http://www.plantuml.com/plantuml/uml)
2. Copia el contenido de cualquier archivo `.puml`
3. Pégalo en el editor y haz clic en "Submit"
4. El diagrama se generará automáticamente

### Opción 2: VS Code con Extensión PlantUML
1. Instala la extensión "PlantUML" en VS Code
2. Abre cualquier archivo `.puml`
3. Presiona `Ctrl+Shift+P` y busca "PlantUML: Preview Current Diagram"
4. O usa `Alt+D` para vista previa

### Opción 3: PlantUML CLI (Local)
```bash
# Instalar PlantUML (requiere Java)
java -jar plantuml.jar diagrama_clases.puml

# Esto generará una imagen PNG del diagrama
```

### Opción 4: Herramientas Online Alternativas
- [PlantText](https://www.planttext.com/)
- [PlantUML QEditor](https://github.com/borisbabic/qplantuml)

## 📐 Patrones de Diseño Documentados

Los diagramas incluyen anotaciones sobre los siguientes patrones:

1. **Repository Pattern**: En ProductoService y UsuarioService
2. **Facade Pattern**: En AuthService para simplificar autenticación
3. **Factory Pattern**: En SessionLocal para crear sesiones de BD
4. **Dependency Injection**: FastAPI inyecta dependencias automáticamente
5. **Composition Pattern**: AuthService compone PasswordManager y TokenManager
6. **Service Layer Pattern**: Capa de servicios encapsula lógica de negocio

## 🎯 Principios SOLID Aplicados

- **S**RP: Cada clase tiene una responsabilidad específica
- **O**CP: Sistema abierto para extensión, cerrado para modificación
- **L**SP: Los esquemas Pydantic son intercambiables
- **I**SP: Interfaces específicas para cada funcionalidad
- **D**IP: Dependencias invertidas mediante inyección

## 📚 Para el Proyecto de FIS

Estos diagramas son perfectos para tu proyecto de Fundamentos de Ingeniería del Software porque:

✅ **Múltiples tipos de diagramas UML**:
- Diagrama de Clases (estructura estática)
- Diagrama de Arquitectura (vista de capas)
- Diagramas de Secuencia (comportamiento dinámico)

✅ **Arquitectura orientada a objetos robusta**:
- 10+ clases principales
- Relaciones claras entre clases
- Patrones de diseño bien definidos

✅ **Documentación profesional**:
- Código bien comentado
- Separación clara de responsabilidades
- Principios de ingeniería de software aplicados

## 🚀 Próximos Pasos

1. **Genera los diagramas** usando cualquiera de las opciones anteriores
2. **Incluye las imágenes** en tu documentación del proyecto
3. **Explica los patrones** utilizados en tu presentación
4. **Destaca la arquitectura** orientada a objetos en tu entrega

¡Estos diagramas te darán una excelente base para demostrar tu comprensión de la ingeniería de software!
