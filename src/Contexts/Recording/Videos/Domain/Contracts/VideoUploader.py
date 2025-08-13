from abc import ABC, abstractmethod
from ..Entities.Video import Video


class VideoUploader(ABC):
    """Contrato para subir videos al almacenamiento externo"""

    @abstractmethod
    def upload_overwrite(self, video: Video, destination_path: str) -> str:
        """
        Sube un video al almacenamiento externo sobrescribiendo si ya existe

        Args:
            video: Video a subir
            destination_path: Ruta de destino en el almacenamiento

        Returns:
            URL o identificador del video subido
        """
        pass
