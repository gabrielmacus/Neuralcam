from dataclasses import dataclass
from datetime import datetime

from src.Contexts.SharedKernel.Domain.DomainEvent import DomainEvent


@dataclass(frozen=True)
class FinishedRecordingSessionDomainEvent(DomainEvent):
    recording_session_id: str
    profile_id: str
    profile_name: str
    start_date: datetime
    end_date: datetime
    duration_seconds: int
    output_path: str

    @property
    def event_name(self) -> str:
        return "recording_session.finished"
