import random
from typing import Optional

from src.Contexts.Recording.RecordingSessions.Domain.ValueObjects.RecordingSessionDuration import (
    RecordingSessionDuration,
)


class RecordingSessionDurationMother:

    @staticmethod
    def create(value: Optional[int] = None) -> RecordingSessionDuration:
        if value is None:
            # Generar duración aleatoria entre 1 minuto (60 segundos) y 2 horas (7200 segundos)
            value = random.randint(60, 7200)
        return RecordingSessionDuration(value)
