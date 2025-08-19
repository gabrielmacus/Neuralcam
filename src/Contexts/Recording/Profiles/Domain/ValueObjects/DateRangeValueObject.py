from __future__ import annotations
from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional


@dataclass(frozen=True)
class DateRangeValueObject:
    """Value object que representa un rango de fechas con año"""
    start_date: date
    end_date: date

    def __post_init__(self):
        if self.start_date > self.end_date:
            raise ValueError(f"La fecha de inicio ({self.start_date}) debe ser anterior a la fecha de fin ({self.end_date})")

    @classmethod
    def from_strings(cls, start_date_str: str, end_date_str: str, date_format: str = "%Y-%m-%d") -> "DateRangeValueObject":
        """Crea DateRangeValueObject desde strings de fecha"""
        try:
            start_date = datetime.strptime(start_date_str, date_format).date()
            end_date = datetime.strptime(end_date_str, date_format).date()
            return cls(start_date, end_date)
        except ValueError as e:
            raise ValueError(f"Error parsing dates: {e}")

    @classmethod
    def from_tuples(cls, start_date_tuple: tuple[int, int, int], end_date_tuple: tuple[int, int, int]) -> "DateRangeValueObject":
        """Crea DateRangeValueObject desde tuplas (año, mes, día)"""
        try:
            start_date = date(start_date_tuple[0], start_date_tuple[1], start_date_tuple[2])
            end_date = date(end_date_tuple[0], end_date_tuple[1], end_date_tuple[2])
            return cls(start_date, end_date)
        except ValueError as e:
            raise ValueError(f"Error creating dates: {e}")

    def contains_date(self, check_date: date) -> bool:
        """Verifica si una fecha está dentro del rango"""
        return self.start_date <= check_date <= self.end_date

    def contains_date_ignoring_year(self, check_date: date) -> bool:
        """
        Verifica si una fecha está dentro del rango ignorando el año.
        Útil para rangos que se repiten anualmente.
        """
        # Convertir las fechas para comparar solo mes y día
        start_month_day = (self.start_date.month, self.start_date.day)
        end_month_day = (self.end_date.month, self.end_date.day)
        check_month_day = (check_date.month, check_date.day)

        # Si el rango no cruza el año (ej: marzo a noviembre)
        if start_month_day <= end_month_day:
            return start_month_day <= check_month_day <= end_month_day
        
        # Si el rango cruza el año (ej: noviembre a marzo del siguiente año)
        return check_month_day >= start_month_day or check_month_day <= end_month_day

    def overlaps_with(self, other: "DateRangeValueObject") -> bool:
        """Verifica si este rango se superpone con otro"""
        return not (self.end_date < other.start_date or other.end_date < self.start_date)

    @property
    def duration_days(self) -> int:
        """Retorna la duración del rango en días"""
        return (self.end_date - self.start_date).days + 1

    @property
    def value(self) -> tuple[date, date]:
        """Retorna la tupla de fechas"""
        return (self.start_date, self.end_date)

    def to_dict(self) -> dict:
        """Convierte a diccionario para serialización"""
        return {
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat()
        }

    @classmethod
    def from_dict(cls, data: dict) -> "DateRangeValueObject":
        """Crea desde diccionario"""
        return cls(
            start_date=date.fromisoformat(data["start_date"]),
            end_date=date.fromisoformat(data["end_date"])
        )

    def __str__(self) -> str:
        return f"Del {self.start_date.strftime('%d de %B de %Y')} al {self.end_date.strftime('%d de %B de %Y')}"