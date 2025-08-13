import uuid
from typing import Optional

from src.Contexts.Recording.RecordingSessions.Domain.ValueObjects.RecordingSessionId import (
    RecordingSessionId,
)


class RecordingSessionIdMother:

    @staticmethod
    def create(value: Optional[str] = None) -> RecordingSessionId:
        if value is None:
            value = str(uuid.uuid4())
        return RecordingSessionId(value)
