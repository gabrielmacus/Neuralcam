from __future__ import annotations

from dataclasses import dataclass

from src.Contexts.SharedKernel.Domain.ValueObjects.DayValueObject import DayValueObject


@dataclass(frozen=True)
class DayRangeValueObject:
    start_day: DayValueObject
    end_day: DayValueObject

    def __init__(self, start_day: tuple[int, int], end_day: tuple[int, int]):
        object.__setattr__(self, "start_day", DayValueObject(start_day[0], start_day[1]))
        object.__setattr__(self, "end_day", DayValueObject(end_day[0], end_day[1]))

    """
    def __ensure_is_valid_day_range(self, start_day: DayValueObject, end_day: DayValueObject):
        if not start_day.is_before(end_day):
            raise ValueError("Start day must be before end day")
            #TODO: raise custom exception
    """

    @property
    def value(self) -> tuple[tuple[int, int], tuple[int, int]]:
        return self.start_day.value, self.end_day.value

    def is_in_range(self, day: int, month: int) -> bool:
        current_day = DayValueObject(day, month)

        if self.start_day.is_equal(current_day) or self.end_day.is_equal(current_day):
            return True

        # For ranges crossing year
        if self.end_day.is_before(self.start_day):
            return current_day.is_after(self.start_day) or current_day.is_before(self.end_day)

        return current_day.is_after(self.start_day) and current_day.is_before(self.end_day)
