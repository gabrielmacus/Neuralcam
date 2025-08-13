import random
from typing import Optional

from src.Contexts.Recording.RecordingSessions.Domain.ValueObjects.Uri import Uri


class UriMother:

    @staticmethod
    def create(value: Optional[str] = None) -> Uri:
        if value is None:
            # Generar URI aleatoria para perfiles de usuario
            user_id = random.randint(1000, 9999)
            value = f"https://example.com/profiles/user_{user_id}"
        return Uri(value)
