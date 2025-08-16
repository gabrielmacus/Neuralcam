from abc import ABC, abstractmethod
from typing import List, Optional
from ..Entities.Video import Video


class VideoRepository(ABC):
    """Contrato para acceder a videos desde el sistema de archivos"""

    @abstractmethod
    def find_videos_in_directory(self, directory_path: str) -> List[Video]:
        """
        Busca todos los videos en un directorio específico

        Args:
            directory_path: Ruta del directorio donde buscar videos

        Returns:
            Lista de videos encontrados
        """
        pass

    @abstractmethod
    def find_by_path(self, video_path: str) -> Optional[Video]:
        """
        Busca un video por su ruta específica

        Args:
            video_path: Ruta completa del video

        Returns:
            Video encontrado o None si no existe
        """
        pass
