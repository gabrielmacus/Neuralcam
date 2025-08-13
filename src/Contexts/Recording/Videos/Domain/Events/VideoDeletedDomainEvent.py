from dataclasses import dataclass
from datetime import datetime
from src.Contexts.SharedKernel.Domain.DomainEvent import DomainEvent


@dataclass(frozen=True)
class VideoDeletedDomainEvent(DomainEvent):
    """Evento de dominio para cuando un video es eliminado después de ser subido"""

    video_id: str
    video_name: str
    video_path: str
    occurred_on: datetime

    @property
    def event_name(self) -> str:
        return "video.deleted"
