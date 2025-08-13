from dataclasses import dataclass


@dataclass(frozen=True)
class StringValueObject:
    value: str

    def __str__(self):
        return self.value
