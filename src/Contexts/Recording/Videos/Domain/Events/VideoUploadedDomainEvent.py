from dataclasses import dataclass
from datetime import datetime
from src.Contexts.SharedKernel.Domain.DomainEvent import DomainEvent


@dataclass(frozen=True)
class VideoUploadedDomainEvent(DomainEvent):
    """Evento de dominio para cuando un video es subido exitosamente"""

    video_id: str
    video_name: str
    upload_destination: str
    occurred_on: datetime

    @property
    def event_name(self) -> str:
        return "video.uploaded"
