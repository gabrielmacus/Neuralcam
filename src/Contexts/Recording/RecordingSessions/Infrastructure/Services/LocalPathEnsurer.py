import os
from pathlib import Path

from src.Contexts.Recording.RecordingSessions.Domain.Contracts.PathEnsurer import PathEnsurer
from src.Contexts.Recording.RecordingSessions.Domain.ValueObjects.OutputPath import OutputPath


class LocalPathEnsurer(PathEnsurer):
    """Servicio de infraestructura que asegura que los paths locales del sistema de archivos existan."""

    def ensure_path(self, output_path: OutputPath) -> None:
        """
        Asegura que el directorio del output_path exista en el sistema de archivos local.

        Args:
            output_path: Path del archivo de salida que debe existir
        """
        directory_path = Path(output_path.value).parent

        if not directory_path.exists():
            os.makedirs(directory_path, exist_ok=True)
