from __future__ import annotations

from dataclasses import dataclass

from src.Contexts.SharedKernel.Domain.ValueObjects.TimeValueObject import TimeValueObject


@dataclass(frozen=True)
class TimeRangeValueObject:
    start_time: TimeValueObject
    end_time: TimeValueObject

    def __init__(self, start_time: tuple[int, int], end_time: tuple[int, int]):
        object.__setattr__(self, "start_time", TimeValueObject(start_time[0], start_time[1]))
        object.__setattr__(self, "end_time", TimeValueObject(end_time[0], end_time[1]))

    """
    def __ensure_is_valid_time_range(self, start_time: TimeValueObject, end_time: TimeValueObject):
        if not start_time.is_before(end_time):
            raise ValueError("Start time must be before end time")
    """

    @property
    def value(self) -> tuple[tuple[int, int], tuple[int, int]]:
        return self.start_time.value, self.end_time.value

    def is_in_range(self, hour: int, minute: int) -> bool:
        current_time = TimeValueObject(hour, minute)

        if current_time.is_equal(self.start_time) or current_time.is_equal(self.end_time):
            return True

        # For ranges crossing midnight
        if self.end_time.is_before(self.start_time):
            return current_time.is_after(self.start_time) or current_time.is_before(self.end_time)

        return current_time.is_after(self.start_time) and current_time.is_before(self.end_time)
