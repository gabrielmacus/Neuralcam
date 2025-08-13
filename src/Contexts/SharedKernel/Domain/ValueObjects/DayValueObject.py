from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DayValueObject:
    day: int
    month: int

    def __post_init__(self):
        self.__ensure_is_valid_day_month_combination(self.day, self.month)

    def __ensure_is_valid_day(self, day: int):
        if day < 1 or day > 31:
            raise ValueError("Invalid day")
            # TODO: raise custom exception

    def __ensure_is_valid_month(self, month: int):
        if month < 1 or month > 12:
            raise ValueError("Invalid month")
            # TODO: raise custom exception

    def __ensure_is_valid_day_month_combination(self, day: int, month: int):
        self.__ensure_is_valid_day(day)
        self.__ensure_is_valid_month(month)
        # Validate day-month combinations to prevent invalid dates like February 31st
        days_in_month = {
            1: 31,  # January
            2: 28,  # February
            3: 31,  # March
            4: 30,  # April
            5: 31,  # May
            6: 30,  # June
            7: 31,  # July
            8: 31,  # August
            9: 30,  # September
            10: 31,  # October
            11: 30,  # November
            12: 31,  # December
        }

        max_days = days_in_month.get(month, 28)
        if day > max_days:
            raise ValueError(f"Invalid day {day} for month {month}")
            # TODO: raise custom exception

    @property
    def value(self) -> tuple[int, int]:
        return self.day, self.month

    def is_before(self, other: "DayValueObject") -> bool:
        return self.month < other.month or (self.day < other.day and self.month == other.month)

    def is_after(self, other: "DayValueObject") -> bool:
        return self.month > other.month or (self.day > other.day and self.month == other.month)

    def is_equal(self, other: "DayValueObject") -> bool:
        return self.month == other.month and self.day == other.day

    def get_value(self) -> tuple[int, int]:
        return self.day, self.month
