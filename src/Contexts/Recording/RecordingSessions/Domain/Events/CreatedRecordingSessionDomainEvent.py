from dataclasses import dataclass
from datetime import datetime

from src.Contexts.SharedKernel.Domain.DomainEvent import DomainEvent


@dataclass(frozen=True)
class CreatedRecordingSessionDomainEvent(DomainEvent):
    recording_session_id: str
    profile_id: str
    profile_name: str
    start_date: datetime
    duration_seconds: int

    @property
    def event_name(self) -> str:
        return "recording_session.created"
