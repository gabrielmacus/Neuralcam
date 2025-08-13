from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TimeValueObject:
    hour: int
    minute: int

    def __post_init__(self):
        self.__ensure_is_valid_hour(self.hour)
        self.__ensure_is_valid_minute(self.minute)

    def __ensure_is_valid_hour(self, hour: int):
        if hour < 0 or hour > 23:
            raise ValueError("Invalid hour: must be between 0 and 23")
            # TODO: raise custom exception

    def __ensure_is_valid_minute(self, minute: int):
        if minute < 0 or minute > 59:
            raise ValueError("Invalid minute: must be between 0 and 59")
            # TODO: raise custom exception

    @property
    def value(self) -> tuple[int, int]:
        return self.hour, self.minute

    def is_before(self, other: "TimeValueObject") -> bool:
        return self.hour < other.hour or (self.hour == other.hour and self.minute < other.minute)

    def is_after(self, other: "TimeValueObject") -> bool:
        return self.hour > other.hour or (self.hour == other.hour and self.minute > other.minute)

    def is_equal(self, other: "TimeValueObject") -> bool:
        return self.hour == other.hour and self.minute == other.minute
