from dataclasses import dataclass

from src.Contexts.SharedKernel.Domain.ValueObjects.StringValueObject import StringValueObject


@dataclass(frozen=True)
class RequiredStringValueObject(StringValueObject):
    def __post_init__(self):
        self.__ensure_is_not_empty(self.value)

    def __ensure_is_not_empty(self, value: str):
        if not value or not value.strip():
            raise ValueError("Value cannot be empty")
