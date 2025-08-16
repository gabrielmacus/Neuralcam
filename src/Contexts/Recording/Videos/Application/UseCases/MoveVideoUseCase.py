from src.Contexts.SharedKernel.Domain.LoggerInterface import LoggerInterface
from src.Contexts.SharedKernel.Domain.EventBusInterface import EventBusInterface
from src.Contexts.SharedKernel.Domain.Configuration import Configuration
from ...Domain.Services.VideoMover import VideoMover
from ...Domain.Services.VideoEnsurer import VideoEnsurer


class MoveVideoUseCase:
    """Caso de uso para mover un video específico (subir y eliminar)"""

    def __init__(
        self,
        video_mover: VideoMover,
        video_ensurer: VideoEnsurer,
        logger: LoggerInterface,
        event_bus: EventBusInterface,
        configuration: Configuration,
    ):
        self._video_mover = video_mover
        self._video_ensurer = video_ensurer
        self._logger = logger
        self._event_bus = event_bus
        self._configuration = configuration

    def execute(self, video_path: str) -> None:
        """
        Ejecuta el proceso de mover un video específico

        Args:
            video_path: Ruta del video a mover
        """
        self._logger.info(f"Iniciando proceso de mover video: {video_path}")
        video = self._video_ensurer.ensure_video(video_path)
        self._logger.info(f"Procesando video: {video.path.value}")

        destination_path = self.__build_destination_path(video_path)
        self._video_mover.move(video, destination_path)

        self._event_bus.publish(video.pull_domain_events())
        self._logger.info(f"Video movido exitosamente: {video.path.value}")

    def __build_destination_path(self, video_path: str) -> str:
        """
        Construye la ruta de destino usando Configuration

        Args:
            video_path: Ruta del video original

        Returns:
            Ruta de destino construida
        """
        base_path = self._configuration.get_string("video_storage_base_path", "/storage/videos")
        filename = video_path.split("/")[-1]
        return f"{base_path}/{filename}"
