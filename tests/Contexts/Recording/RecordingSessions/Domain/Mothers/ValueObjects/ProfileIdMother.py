import uuid
from typing import Optional

from src.Contexts.Recording.RecordingSessions.Domain.ValueObjects.ProfileId import ProfileId


class ProfileIdMother:

    @staticmethod
    def create(value: Optional[str] = None) -> ProfileId:
        if value is None:
            value = str(uuid.uuid4())
        return ProfileId(value)
