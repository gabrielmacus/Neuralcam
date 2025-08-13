# Módulo Videos

Este módulo forma parte del contexto Recording y se encarga de gestionar videos generados por el módulo RecordingSessions.

## Funcionalidades

### ✅ Lectura de Videos
- Lee videos desde el sistema de archivos (no desde base de datos)
- Busca videos en directorios específicos
- Filtra videos por patrones (ej: `*.mkv`, `profile_*`)
- Soporta múltiples formatos: .mkv, .mp4, .avi, .mov, .wmv, .flv, .webm, .m4v

### ✅ Subida y Eliminación
- Sube videos a almacenamiento externo
- Elimina videos locales después de subirlos exitosamente
- Maneja errores y rollback en caso de fallos
- Registra eventos de dominio para auditoría

### ✅ Arquitectura Hexagonal
- **Domain**: Entidades, Value Objects, Servicios, Contratos, Eventos, Excepciones
- **Application**: Casos de Uso, DTOs, Queries
- **Infrastructure**: Implementaciones concretas de los contratos

## Estructura del Módulo

```
Videos/
├── Domain/
│   ├── Entities/
│   │   └── Video.py                    # Aggregate Root
│   ├── ValueObjects/
│   │   ├── VideoId.py
│   │   ├── VideoPath.py
│   │   ├── VideoName.py
│   │   └── VideoExtension.py
│   ├── Services/
│   │   └── VideoService.py             # Lógica de subida y eliminación
│   ├── Contracts/
│   │   ├── VideoRepository.py
│   │   ├── VideoUploader.py
│   │   └── VideoDeleter.py
│   ├── Events/
│   │   ├── VideoUploadedDomainEvent.py
│   │   └── VideoDeletedDomainEvent.py
│   └── Exceptions/
│       ├── VideoNotFoundException.py
│       ├── VideoUploadFailedException.py
│       └── VideoFileOperationException.py
├── Application/
│   ├── UseCases/
│   │   ├── ListVideosUseCase.py
│   │   └── UploadAndDeleteVideoUseCase.py
│   ├── DTO/
│   │   └── VideoDTO.py
│   └── Queries/
│       ├── GetVideosQuery.py
│       └── GetVideosQueryResponse.py
└── Infrastructure/
    └── Services/
        ├── LocalVideoRepository.py     # Lee videos del sistema de archivos
        ├── LocalVideoDeleter.py        # Elimina archivos locales
        └── DummyVideoUploader.py       # Implementación dummy para pruebas
```

## Entidad Video (Aggregate Root)

```python
class Video:
    # Propiedades básicas como solicitado
    - id: VideoId
    - path: VideoPath      # Ruta completa del archivo
    - name: VideoName      # Nombre sin extensión
    - extension: VideoExtension
    
    # Métodos principales
    + exists() -> bool
    + file_size() -> int
    + get_full_filename() -> str
```

## Casos de Uso Principales

### 1. Listar Videos
```python
# Listar todos los videos en un directorio
query = GetVideosQuery(directory_path="/recordings")
response = list_videos_use_case.handle(query)

# Listar videos con patrón específico
query = GetVideosQuery(directory_path="/recordings", pattern="*.mkv")
response = list_videos_use_case.handle(query)
```

### 2. Subir y Eliminar Video
```python
# Procesar un video (subir al almacenamiento y eliminar local)
upload_result = upload_and_delete_use_case.execute(
    video_path="/recordings/video.mkv",
    destination_path="uploads/2024"
)
```

## Implementaciones de Infraestructura

### LocalVideoRepository
- Lee videos desde directorios del sistema de archivos
- Filtra por extensiones soportadas
- Busca por patrones usando glob

### LocalVideoDeleter
- Elimina archivos locales siguiendo la interfaz VideoDeleter
- Valida existencia y tipo de archivo antes de eliminar
- Registro detallado de operaciones de eliminación

### DummyVideoUploader
- Implementación de prueba que simula subida con sobrescritura
- Usa método upload_overwrite() para subir videos sobrescribiendo si ya existen
- En producción se reemplazaría por implementación real (AWS S3, Google Cloud, etc.)
- Simula progreso de subida y genera URLs ficticias

## Eventos de Dominio

### VideoUploadedDomainEvent
Se dispara cuando un video se sube exitosamente:
- video_id
- video_name
- video_path
- upload_destination
- file_size
- occurred_on

### VideoDeletedDomainEvent
Se dispara cuando un video se elimina del sistema local:
- video_id
- video_name
- video_path
- occurred_on

## Integración con RecordingSessions

El módulo Videos está diseñado para procesar videos generados por RecordingSessions:

1. RecordingSessions genera videos en directorios específicos
2. Videos lee esos directorios automáticamente
3. Videos puede procesar los videos (subir y eliminar) de forma asíncrona
4. Los eventos de dominio permiten coordinar entre módulos

## Extensibilidad

### Para agregar nuevos formatos de video:
Modificar `VideoExtension.SUPPORTED_EXTENSIONS`

### Para cambiar el almacenamiento:
Crear nueva implementación de `VideoUploader` (ej: S3VideoUploader, AzureVideoUploader)

### Para agregar metadatos:
Extender la entidad `Video` con nuevos value objects según necesidades

## Principios Seguidos

- **Single Responsibility**: Cada clase tiene una responsabilidad específica
- **Open/Closed**: Extensible mediante nuevas implementaciones de contratos
- **Dependency Inversion**: Depende de abstracciones, no de concreciones
- **Domain-Driven Design**: Lenguaje ubicuo y separación de capas
- **CQRS**: Separación entre comandos (casos de uso) y consultas (queries) 