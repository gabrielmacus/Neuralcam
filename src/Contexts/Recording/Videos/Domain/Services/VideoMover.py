from src.Contexts.SharedKernel.Domain.LoggerInterface import LoggerInterface
from ..Entities.Video import Video
from ..Contracts.VideoFileManager import VideoFileManager
from ..Contracts.VideoUploader import VideoUploader
from ..Exceptions.VideoUploadFailedException import VideoUploadFailedException
from ..Exceptions.VideoFileOperationException import VideoFileOperationException
from ..Exceptions.VideoNotFoundException import VideoNotFoundException


class VideoMover:
    """Servicio de dominio para mover videos (subir, copiar y eliminar)"""

    def __init__(
        self,
        video_file_manager: VideoFileManager,
        video_uploader: VideoUploader,
        logger: LoggerInterface,
    ):
        self._video_file_manager = video_file_manager
        self._video_uploader = video_uploader
        self._logger = logger

    def move(self, video: Video, destination_path: str) -> str:
        """
        Mueve un video completamente: sube al almacenamiento y elimina el original

        Args:
            video: Video a mover
            destination_path: Ruta de destino en el almacenamiento

        Returns:
            URL o identificador del video subido

        Raises:
            VideoNotFoundException: Si el archivo de video no existe
            VideoUploadFailedException: Si falla la subida
            VideoFileOperationException: Si falla la operación de archivos
        """
        try:
            self._logger.info(f"Iniciando proceso completo de mover video: {video.path.value}")

            self.__ensure_video_exists(video)

            # Subir el video
            upload_result = self._video_uploader.upload_overwrite(video, destination_path)
            video.mark_as_uploaded(upload_result)

            # Eliminar archivo original
            self._video_file_manager.delete(video)
            video.mark_as_deleted()

            self._logger.info(f"Video movido completamente: {video.path.value}")
            return upload_result

        except VideoNotFoundException:
            # Re-lanzar la excepción de dominio tal como está
            raise
        except Exception as e:
            self._logger.error(f"Error al mover video {video.path.value}: {str(e)}")
            raise VideoFileOperationException(f"Error al mover video: {str(e)}", e)

    def __ensure_video_exists(self, video: Video) -> None:
        """
        Verifica que el archivo de video exista antes de intentar subirlo

        Args:
            video: Video a verificar

        Raises:
            VideoNotFoundException: Si el archivo de video no existe
        """
        if not self._video_file_manager.exists(video):
            raise VideoNotFoundException(f"El archivo de video no existe: {video.path.value}")
