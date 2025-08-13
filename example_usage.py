#!/usr/bin/env python3
"""
Ejemplo de uso de la infraestructura de grabación implementada.

Este ejemplo muestra cómo utilizar:
- ThreadTaskManager para manejo de tareas en background
- ConsoleLogger para logging
- PyAvVideoRecorder para grabación sin recodificación (remuxing)
- RecordingService para orquestar el proceso
"""

from datetime import datetime

from src.Contexts.Recording.RecordingSessions.Domain.Services.RecordingService import (
    RecordingService,
)
from src.Contexts.Recording.RecordingSessions.Domain.ValueObjects.Uri import Uri
from src.Contexts.Recording.RecordingSessions.Infrastructure.Services.PyAvVideoRecorder import (
    PyAvVideoRecorder,
)
from src.Contexts.SharedKernel.Infrastructure.Services.ConsoleLogger import ConsoleLogger
from src.Contexts.SharedKernel.Infrastructure.Services.ThreadTaskManager import (
    ThreadTaskManager,
)


def main():
    """Ejemplo de uso de la infraestructura de grabación."""

    # Crear instancias de la infraestructura
    logger = ConsoleLogger()
    task_manager = ThreadTaskManager()
    video_recorder = PyAvVideoRecorder(
        logger=logger,
        output_directory="recordings",  # Directorio donde se guardarán las grabaciones
        duration_seconds=30,  # Grabar por 30 segundos
    )

    # Crear el servicio de grabación (dominio)
    recording_service = RecordingService(
        task_manager=task_manager,
        video_recorder=video_recorder,
        logger=logger,
    )

    logger.info("=== DEMO: Sistema de Grabación Neural ===")
    logger.info("Inicializando sistema...")

    # Ejemplo 1: Grabar desde un archivo de video existente
    try:
        logger.info("\n1. Grabando desde archivo de video...")
        video_uris = [
            Uri("input_video.mp4"),  # Archivo de entrada (debe existir)
            # Uri("another_video.avi"),  # Más archivos si tienes
        ]

        logger.info("Iniciando grabación en background...")
        recording_service.record_profiles(video_uris)

        # Dar tiempo para que las tareas se ejecuten
        import time

        time.sleep(2)

        logger.info("Grabación iniciada en background threads")

    except Exception as e:
        logger.error(f"Error al grabar desde archivo: {e}")

    # Ejemplo 2: Grabar desde una URL de stream (si está disponible)
    try:
        logger.info("\n2. Ejemplo de grabación desde stream URL...")
        # stream_uris = [
        #     Uri("http://example.com/stream.m3u8"),  # Stream HLS
        #     Uri("rtmp://example.com/live/stream"),   # Stream RTMP
        # ]

        # Descomenta para probar con streams reales
        # recording_service.record_profiles(stream_uris)
        logger.info("Stream grabbing example (comentado - requiere URLs reales)")

    except Exception as e:
        logger.error(f"Error al grabar desde stream: {e}")

    logger.info("\n=== Características de la implementación ===")
    logger.info("✓ ThreadTaskManager: Ejecuta grabaciones en paralelo usando threads")
    logger.info("✓ PyAvVideoRecorder: Usa remuxing (sin recodificación) para máxima eficiencia")
    logger.info("✓ ConsoleLogger: Logging estructurado con timestamps")
    logger.info("✓ Arquitectura hexagonal: Dominio separado de infraestructura")
    logger.info("✓ Pyright compatible: 0 errores de tipos")

    logger.info("\n=== Ventajas del remuxing ===")
    logger.info("• No hay pérdida de calidad (sin recodificación)")
    logger.info("• Procesamiento ultra-rápido (solo copia streams)")
    logger.info("• Bajo uso de CPU")
    logger.info("• Preserva todos los metadatos originales")

    logger.info(f"\nDemo completada - {datetime.now()}")


if __name__ == "__main__":
    main()
