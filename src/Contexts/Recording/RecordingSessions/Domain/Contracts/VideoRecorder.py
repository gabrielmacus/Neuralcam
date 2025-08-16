from abc import ABC, abstractmethod
from typing import Callable, Optional

from ..ValueObjects.Uri import Uri
from ..ValueObjects.OutputPath import OutputPath
from ..ValueObjects.RecordingSessionDuration import RecordingSessionDuration


class VideoRecorder(ABC):
    @abstractmethod
    def record(
        self,
        uri: Uri,
        output_path: OutputPath,
        duration_seconds: RecordingSessionDuration,
        on_finished: Optional[Callable[[str], None]] = None,
    ) -> None:
        """
        Graba video desde una URI por una duración específica

        Args:
            uri: URI del video a grabar
            output_path: Ruta donde guardar el video grabado
            duration_seconds: Duración de la grabación en segundos
            on_finished: Callback opcional que se ejecuta cuando termina la grabación
                        Recibe como parámetro la ruta del archivo grabado
        """
        pass
