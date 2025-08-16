from src.Contexts.SharedKernel.Domain.LoggerInterface import LoggerInterface
from ...Domain.Events.FinishedRecordingSessionIntegrationEvent import (
    FinishedRecordingSessionIntegrationEvent,
)
from ..UseCases.MoveVideoUseCase import MoveVideoUseCase


class MoveVideoOnFinishedRecordingSession:
    """Event handler que mueve videos cuando termina una sesión de grabación"""

    def __init__(
        self,
        move_video_use_case: MoveVideoUseCase,
        logger: LoggerInterface,
    ):
        self._move_video_use_case = move_video_use_case
        self._logger = logger

    def handle(self, event: FinishedRecordingSessionIntegrationEvent) -> None:
        """
        Maneja el evento de sesión de grabación finalizada moviendo el video

        Args:
            event: Evento de sesión de grabación finalizada
        """
        self._logger.debug(
            f"Manejando evento de sesión finalizada para mover video: {event.output_path}"
        )
        self._move_video_use_case.execute(event.output_path)
