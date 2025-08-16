from ..Contracts.VideoRepository import VideoRepository
from ..Entities.Video import Video
from ..Exceptions.VideoNotFoundException import VideoNotFoundException


class VideoEnsurer:
    """Servicio de dominio para asegurar que un video existe"""

    def __init__(self, video_repository: VideoRepository):
        self._video_repository = video_repository

    def ensure_video(self, path: str) -> Video:
        """
        Asegura que un video existe en la ruta especificada

        Args:
            path: Ruta del video a verificar

        Returns:
            Video encontrado

        Raises:
            VideoNotFoundException: Si el video no existe
        """
        video = self._video_repository.find_by_path(path)
        if not video:
            raise VideoNotFoundException(f"Video no encontrado en la ruta: {path}")
        return video
