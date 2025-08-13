from datetime import datetime
from typing import Optional

from src.Contexts.Recording.RecordingSessions.Domain.Entities.RecordingSession import (
    RecordingSession,
)

from .ValueObjects.ProfileIdMother import ProfileIdMother
from .ValueObjects.RecordingSessionDurationMother import RecordingSessionDurationMother
from .ValueObjects.RecordingSessionIdMother import RecordingSessionIdMother
from .ValueObjects.StartDateMother import StartDateMother
from .ValueObjects.UriMother import UriMother


class RecordingSessionMother:

    @staticmethod
    def create(
        recording_session_id: Optional[str] = None,
        profile_id: Optional[str] = None,
        start_date: Optional[datetime] = None,
        duration_seconds: Optional[int] = None,
        profile_uri: Optional[str] = None,
    ) -> RecordingSession:

        # Usar object mothers para generar valores si no se proporcionan
        if recording_session_id is None:
            recording_session_id = RecordingSessionIdMother.create().value

        if profile_id is None:
            profile_id = ProfileIdMother.create().value

        if start_date is None:
            start_date = StartDateMother.create().value

        if duration_seconds is None:
            duration_seconds = RecordingSessionDurationMother.create().value

        if profile_uri is None:
            profile_uri = UriMother.create().value

        return RecordingSession.create(
            recording_session_id=recording_session_id,
            profile_id=profile_id,
            start_date=start_date,
            duration_seconds=duration_seconds,
            profile_uri=profile_uri,
        )
