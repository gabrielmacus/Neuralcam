import os
from src.Contexts.SharedKernel.Domain.LoggerInterface import LoggerInterface
from ...Domain.Contracts.VideoFileManager import VideoFileManager
from ...Domain.Entities.Video import Video


class LocalVideoFileManager(VideoFileManager):
    """Implementación de VideoFileManager para gestionar archivos de video en el sistema local"""

    def __init__(self, logger: LoggerInterface):
        self._logger = logger

    def delete(self, video: Video) -> bool:
        """
        Elimina el archivo de video del sistema de archivos

        Args:
            video: Video a eliminar

        Returns:
            True si se eliminó exitosamente, False en caso contrario
        """
        try:
            file_path = video.path.value

            if not self._file_exists_and_is_valid(file_path):
                return False

            os.remove(file_path)

            if os.path.exists(file_path):
                self._logger.error(f"El archivo no se pudo eliminar: {file_path}")
                return False

            self._logger.info(f"Archivo eliminado exitosamente: {file_path}")
            return True

        except Exception as e:
            self._logger.error(f"Error al eliminar archivo {video.path.value}: {str(e)}")
            return False

    def exists(self, video: Video) -> bool:
        """
        Verifica si el archivo de video existe en el sistema de archivos

        Args:
            video: Video a verificar

        Returns:
            True si el archivo existe y es válido, False en caso contrario
        """
        file_path = video.path.value
        return self._file_exists_and_is_valid(file_path)

    def _file_exists_and_is_valid(self, file_path: str) -> bool:
        """Verifica si un archivo existe y es válido, registrando advertencias si no lo es"""
        if not os.path.exists(file_path):
            self._logger.warn(f"El archivo no existe: {file_path}")
            return False

        if not os.path.isfile(file_path):
            self._logger.warn(f"La ruta no es un archivo: {file_path}")
            return False

        return True
