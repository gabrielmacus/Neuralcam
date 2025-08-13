from abc import ABC, abstractmethod
from typing import List
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
