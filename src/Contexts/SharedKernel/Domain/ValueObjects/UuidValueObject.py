import uuid
from dataclasses import dataclass


@dataclass(frozen=True)
class UuidValueObject:
    value: str

    def __post_init__(self):
        self.ensure_is_valid(self.value)

    def __str__(self):
        return self.value

    def ensure_is_valid(self, value: str):
        if not uuid.UUID(value):
            raise ValueError("Invalid UUID")
