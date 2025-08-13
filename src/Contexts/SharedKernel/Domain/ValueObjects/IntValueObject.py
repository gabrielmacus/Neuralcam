from dataclasses import dataclass


@dataclass(frozen=True)
class IntValueObject:
    value: int

    def __str__(self):
        return str(self.value)
