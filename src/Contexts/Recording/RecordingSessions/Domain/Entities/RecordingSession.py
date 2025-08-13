from datetime import datetime, timedelta

from src.Contexts.SharedKernel.Domain.AggregateRoot import AggregateRoot

from ..Events.CreatedRecordingSessionDomainEvent import CreatedRecordingSessionDomainEvent
from ..ValueObjects.RecordingSessionId import RecordingSessionId
from ..ValueObjects.StartDate import StartDate
from .Profile import Profile


class RecordingSession(AggregateRoot):

    def __init__(
        self,
        recording_session_id: str,
        profile: Profile,
        start_date: datetime,
    ):
        super().__init__()
        self._id = RecordingSessionId(recording_session_id)
        self._profile = profile
        self._start_date = StartDate(start_date)
        self._created_at = datetime.now()

    @classmethod
    def create(
        cls,
        recording_session_id: str,
        profile: Profile,
        start_date: datetime,
    ) -> "RecordingSession":
        recording_session = cls(
            recording_session_id,
            profile,
            start_date,
        )

        # Registrar evento de dominio
        event = CreatedRecordingSessionDomainEvent(
            recording_session_id=recording_session_id,
            profile_id=profile.id.value,
            profile_name=profile.name.value,
            start_date=start_date,
            duration_seconds=profile.duration.value,
        )
        recording_session.record_domain_event(event)

        return recording_session

    def get_end_datetime(self) -> datetime:
        return self._start_date.value + timedelta(seconds=self._profile.duration.value)

    def is_overlapping_with(self, other_start: datetime, other_duration_seconds: int) -> bool:
        other_end = other_start + timedelta(seconds=other_duration_seconds)
        session_end = self.get_end_datetime()

        # Verificar si hay solapamiento
        return not (other_end <= self._start_date.value or other_start >= session_end)

    def is_recording_complete(self) -> bool:
        """Verifica si la grabación ha finalizado"""
        return datetime.now() >= self.get_end_datetime()

    def get_remaining_time_seconds(self) -> int:
        """Obtiene el tiempo restante de grabación en segundos"""
        if self.is_recording_complete():
            return 0

        remaining_time = self.get_end_datetime() - datetime.now()
        return max(0, int(remaining_time.total_seconds()))

    # Propiedades de solo lectura
    @property
    def id(self) -> RecordingSessionId:
        return self._id

    @property
    def profile(self) -> Profile:
        return self._profile

    @property
    def start_date(self) -> StartDate:
        return self._start_date

    @property
    def created_at(self) -> datetime:
        return self._created_at

    # Propiedades delegadas al perfil para mantener compatibilidad
    @property
    def profile_id(self):
        return self._profile.id

    @property
    def profile_name(self):
        return self._profile.name

    @property
    def profile_uri(self):
        return self._profile.uri

    @property
    def duration(self):
        return self._profile.duration

    def __str__(self) -> str:
        return f"RecordingSession({self._id.value}, {self._profile.name.value})"

    def __repr__(self) -> str:
        return f"RecordingSession(id={self._id.value}, profile={self._profile.name.value}, start={self._start_date.value})"
