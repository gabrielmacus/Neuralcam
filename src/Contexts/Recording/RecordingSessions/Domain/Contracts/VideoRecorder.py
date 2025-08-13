from abc import ABC, abstractmethod

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
    ) -> None:
        pass
