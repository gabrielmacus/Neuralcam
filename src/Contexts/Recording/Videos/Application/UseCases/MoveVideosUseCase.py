from src.Contexts.SharedKernel.Domain.LoggerInterface import LoggerInterface
from src.Contexts.SharedKernel.Domain.UuidGenerator import UuidGenerator
from src.Contexts.SharedKernel.Domain.EventBusInterface import EventBusInterface
from ...Domain.Contracts.VideoRepository import VideoRepository
from ...Domain.Services.VideoMover import VideoMover
from ...Domain.Entities.Video import Video


class MoveVideosUseCase:
    """Caso de uso para leer todos los videos de un directorio y moverlos (subir y eliminar)"""

    def __init__(
        self,
        video_repository: VideoRepository,
        video_mover: VideoMover,
        logger: LoggerInterface,
        uuid_generator: UuidGenerator,
        event_bus: EventBusInterface,
    ):
        self._video_repository = video_repository
        self._video_mover = video_mover
        self._logger = logger
        self._uuid_generator = uuid_generator
        self._event_bus = event_bus

    def execute(self, directory_path: str, destination_path: str) -> tuple[int, int]:
        """
        Ejecuta el proceso de mover todos los videos de un directorio

        Args:
            directory_path: Directorio donde buscar los videos
            destination_path: Ruta de destino en el almacenamiento
        """
        self._logger.info(f"Iniciando proceso de mover videos desde directorio: {directory_path}")
        videos = self._video_repository.find_videos_in_directory(directory_path)
        if not videos:
            return 0, 0

        self._logger.info(f"Encontrados {len(videos)} videos para procesar")

        processed_count = 0
        failed_count = 0

        for video in videos:
            try:
                self._logger.info(
                    f"Procesando video {processed_count + 1}/{len(videos)}: {video.path.value}"
                )
                self.__move_video(video, destination_path)
                processed_count += 1
            except Exception as video_error:
                self._logger.error(
                    f"Error al procesar video {video.path.value}: {str(video_error)}"
                )
                failed_count += 1
                continue

        self._logger.info(
            f"Proceso completado. Exitosos: {processed_count}, Fallidos: {failed_count}, Total: {len(videos)}"
        )
        return processed_count, failed_count

    def __move_video(self, video: Video, destination_path: str) -> None:
        self._video_mover.move(video, destination_path)
        self._event_bus.publish(video.pull_domain_events())
