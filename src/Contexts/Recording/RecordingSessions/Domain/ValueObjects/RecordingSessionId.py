from dataclasses import dataclass

from src.Contexts.SharedKernel.Domain.ValueObjects.UuidValueObject import UuidValueObject


@dataclass(frozen=True)
class RecordingSessionId(UuidValueObject):
    pass
