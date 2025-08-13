from abc import ABC, abstractmethod
from ..Entities.Video import Video


class VideoFileManager(ABC):
    """Contrato para gestionar archivos de video (eliminar y verificar existencia)"""

    @abstractmethod
    def delete(self, video: Video) -> bool:
        """
        Elimina el archivo de video del sistema de archivos

        Args:
            video: Video a eliminar

        Returns:
            True si se eliminó exitosamente, False en caso contrario
        """
        pass

    @abstractmethod
    def exists(self, video: Video) -> bool:
        """
        Verifica si el archivo de video existe en el sistema de archivos

        Args:
            video: Video a verificar

        Returns:
            True si el archivo existe, False en caso contrario
        """
        pass
