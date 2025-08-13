# Neuralcam

Sistema de grabación de cámara neural con arquitectura hexagonal y Domain-Driven Design.

## Configuración del entorno de desarrollo

### Instalación de dependencias

```bash
# Instalar dependencias de desarrollo
make install-dev

# O manualmente
pip install -e ".[dev]"
```

### Herramientas de desarrollo

El proyecto incluye las siguientes herramientas de desarrollo:

- **Pyright**: Verificador de tipos estático para Python
- **Black**: Formateador de código automático
- **isort**: Organizador de imports
- **Flake8**: Linter para verificación de estilo

### Comandos disponibles

```bash
# Ver todos los comandos disponibles
make help

# Configurar entorno de desarrollo
make dev-setup

# Verificar tipos con Pyright
make type-check

# Verificar estilo con Flake8
make lint

# Ejecutar todas las verificaciones
make check

# Formatear código automáticamente
make format

# Verificar si el código está formateado correctamente
make format-check

# Limpiar archivos temporales
make clean
```

### Verificación de tipos con Pyright

Pyright está configurado para verificar el directorio `src/` con las siguientes características:

- **Modo de verificación**: Básico
- **Versión de Python**: 3.8+
- **Plataforma**: Linux
- **Reportes habilitados**:
  - Imports faltantes
  - Variables no utilizadas
  - Imports duplicados
  - Type casts innecesarios
  - Ciclos de import
  - Uso de elementos privados

## Estructura del proyecto

```
src/
├── Contexts/
│   ├── Recording/
│   │   └── RecordingSessions/
│   │       ├── Application/
│   │       └── Domain/
│   │           ├── Contracts/
│   │           ├── Entities/
│   │           ├── Events/
│   │           ├── Services/
│   │           └── ValueObjects/
│   └── SharedKernel/
│       └── Domain/
```

## Arquitectura

El proyecto sigue los principios de:

- **Arquitectura Hexagonal**: Separación clara entre dominio, aplicación e infraestructura
- **Domain-Driven Design**: Modelado basado en el dominio del negocio
- **CQRS**: Separación de comandos y queries
- **Event Sourcing**: Manejo de eventos de dominio

## Desarrollo

### Antes de hacer commit

Siempre ejecuta antes de hacer commit:

```bash
make check
```

Esto ejecutará la verificación de tipos y el linting para asegurar que el código cumple con los estándares del proyecto. 