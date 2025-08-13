from abc import ABC, abstractmethod

from Contexts.Recording.RecordingSessions.Domain.ValueObjects.OutputPath import OutputPath


class PathEnsurer(ABC):
    @abstractmethod
    def ensure_path(self, output_path: OutputPath) -> None:
        pass
