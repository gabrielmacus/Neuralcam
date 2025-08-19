from __future__ import annotations
from dataclasses import dataclass
from typing import List, Set
from enum import Enum


class WeekDay(Enum):
    """Enum para los días de la semana"""
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6

    @classmethod
    def from_string(cls, day_str: str) -> "WeekDay":
        """Crea un WeekDay desde string en español"""
        day_mapping = {
            "lunes": cls.MONDAY,
            "martes": cls.TUESDAY,
            "miércoles": cls.WEDNESDAY,
            "miercoles": cls.WEDNESDAY,  # Sin tilde
            "jueves": cls.THURSDAY,
            "viernes": cls.FRIDAY,
            "sábado": cls.SATURDAY,
            "sabado": cls.SATURDAY,  # Sin tilde
            "domingo": cls.SUNDAY
        }
        
        normalized_day = day_str.lower().strip()
        if normalized_day not in day_mapping:
            raise ValueError(f"Día inválido: {day_str}. Debe ser uno de: {', '.join(day_mapping.keys())}")
        
        return day_mapping[normalized_day]

    def to_spanish(self) -> str:
        """Convierte el día a string en español"""
        spanish_names = {
            WeekDay.MONDAY: "lunes",
            WeekDay.TUESDAY: "martes", 
            WeekDay.WEDNESDAY: "miércoles",
            WeekDay.THURSDAY: "jueves",
            WeekDay.FRIDAY: "viernes",
            WeekDay.SATURDAY: "sábado",
            WeekDay.SUNDAY: "domingo"
        }
        return spanish_names[self]


@dataclass(frozen=True)
class WeekDaysValueObject:
    """Value object que representa un conjunto de días de la semana"""
    days: Set[WeekDay]

    def __init__(self, days: List[WeekDay]):
        if not days:
            raise ValueError("Debe especificar al menos un día de la semana")
        
        # Validar que todos los elementos sean WeekDay
        for day in days:
            if not isinstance(day, WeekDay):
                raise ValueError(f"Todos los elementos deben ser de tipo WeekDay, encontrado: {type(day)}")
        
        object.__setattr__(self, "days", set(days))

    @classmethod
    def from_strings(cls, day_strings: List[str]) -> "WeekDaysValueObject":
        """Crea WeekDaysValueObject desde una lista de strings en español"""
        week_days = [WeekDay.from_string(day_str) for day_str in day_strings]
        return cls(week_days)

    @classmethod
    def from_weekday_numbers(cls, weekday_numbers: List[int]) -> "WeekDaysValueObject":
        """Crea WeekDaysValueObject desde números de día (0=lunes, 6=domingo)"""
        week_days = []
        for num in weekday_numbers:
            if num < 0 or num > 6:
                raise ValueError(f"Número de día inválido: {num}. Debe estar entre 0 y 6")
            week_days.append(WeekDay(num))
        return cls(week_days)

    def contains_day(self, weekday_number: int) -> bool:
        """Verifica si contiene un día específico (0=lunes, 6=domingo)"""
        if weekday_number < 0 or weekday_number > 6:
            return False
        return WeekDay(weekday_number) in self.days

    def contains_weekday(self, week_day: WeekDay) -> bool:
        """Verifica si contiene un día específico"""
        return week_day in self.days

    @property
    def value(self) -> Set[int]:
        """Retorna el conjunto de números de día"""
        return {day.value for day in self.days}

    def to_spanish_list(self) -> List[str]:
        """Retorna lista de días en español ordenada"""
        sorted_days = sorted(self.days, key=lambda x: x.value)
        return [day.to_spanish() for day in sorted_days]

    def __str__(self) -> str:
        return ", ".join(self.to_spanish_list())