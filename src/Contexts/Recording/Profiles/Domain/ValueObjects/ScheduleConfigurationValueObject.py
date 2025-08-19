from __future__ import annotations
from dataclasses import dataclass
from datetime import date, datetime, time
from typing import Optional

from src.Contexts.Recording.Profiles.Domain.ValueObjects.DateRangeValueObject import DateRangeValueObject
from src.Contexts.Recording.Profiles.Domain.ValueObjects.WeekDaysValueObject import WeekDaysValueObject
from src.Contexts.SharedKernel.Domain.ValueObjects.TimeRangeValueObject import TimeRangeValueObject


@dataclass(frozen=True)
class ScheduleConfigurationValueObject:
    """
    Value object que representa la configuración completa de horario de un perfil.
    Incluye rango de fechas, rango de horas y días de la semana.
    """
    date_range: Optional[DateRangeValueObject]
    time_range: Optional[TimeRangeValueObject]  
    week_days: Optional[WeekDaysValueObject]

    def __post_init__(self):
        # Al menos una configuración debe estar presente
        if not any([self.date_range, self.time_range, self.week_days]):
            raise ValueError("Debe especificar al menos una configuración de horario (fechas, horas o días)")

    @classmethod
    def create_full_schedule(
        cls,
        date_range: DateRangeValueObject,
        time_range: TimeRangeValueObject,
        week_days: WeekDaysValueObject
    ) -> "ScheduleConfigurationValueObject":
        """Crea una configuración completa con todos los parámetros"""
        return cls(date_range=date_range, time_range=time_range, week_days=week_days)

    @classmethod
    def create_date_only(cls, date_range: DateRangeValueObject) -> "ScheduleConfigurationValueObject":
        """Crea configuración solo con rango de fechas"""
        return cls(date_range=date_range, time_range=None, week_days=None)

    @classmethod
    def create_time_only(cls, time_range: TimeRangeValueObject) -> "ScheduleConfigurationValueObject":
        """Crea configuración solo con rango de horas"""
        return cls(date_range=None, time_range=time_range, week_days=None)

    @classmethod
    def create_weekdays_only(cls, week_days: WeekDaysValueObject) -> "ScheduleConfigurationValueObject":
        """Crea configuración solo con días de la semana"""
        return cls(date_range=None, time_range=None, week_days=week_days)

    def is_active_at(self, check_datetime: datetime) -> bool:
        """
        Determina si la configuración está activa en una fecha/hora dada.
        Todas las condiciones especificadas deben cumplirse.
        """
        check_date = check_datetime.date()
        check_time = check_datetime.time()
        check_weekday = check_datetime.weekday()  # 0=Monday, 6=Sunday

        # Verificar rango de fechas si está especificado
        if self.date_range is not None:
            if not self.date_range.contains_date(check_date):
                return False

        # Verificar rango de horas si está especificado
        if self.time_range is not None:
            if not self.time_range.is_in_range(check_time.hour, check_time.minute):
                return False

        # Verificar días de la semana si están especificados
        if self.week_days is not None:
            if not self.week_days.contains_day(check_weekday):
                return False

        return True

    def is_active_at_date(self, check_date: date) -> bool:
        """Verifica solo la condición de fecha"""
        if self.date_range is None:
            return True
        return self.date_range.contains_date(check_date)

    def is_active_at_time(self, check_time: time) -> bool:
        """Verifica solo la condición de hora"""
        if self.time_range is None:
            return True
        return self.time_range.is_in_range(check_time.hour, check_time.minute)

    def is_active_on_weekday(self, weekday: int) -> bool:
        """Verifica solo la condición de día de la semana"""
        if self.week_days is None:
            return True
        return self.week_days.contains_day(weekday)

    def to_dict(self) -> dict:
        """Convierte a diccionario para serialización"""
        return {
            "date_range": self.date_range.to_dict() if self.date_range else None,
            "time_range": self.time_range.value if self.time_range else None,
            "week_days": list(self.week_days.value) if self.week_days else None
        }

    @classmethod
    def from_dict(cls, data: dict) -> "ScheduleConfigurationValueObject":
        """Crea desde diccionario"""
        date_range = None
        if data.get("date_range"):
            date_range = DateRangeValueObject.from_dict(data["date_range"])

        time_range = None
        if data.get("time_range"):
            start_time, end_time = data["time_range"]
            time_range = TimeRangeValueObject(start_time, end_time)

        week_days = None
        if data.get("week_days"):
            week_days = WeekDaysValueObject.from_weekday_numbers(data["week_days"])

        return cls(date_range=date_range, time_range=time_range, week_days=week_days)

    def __str__(self) -> str:
        """Representación en string amigable"""
        parts = []
        
        if self.date_range:
            parts.append(str(self.date_range))
        
        if self.time_range:
            start_h, start_m = self.time_range.start_time.value
            end_h, end_m = self.time_range.end_time.value
            parts.append(f"de {start_h:02d}:{start_m:02d} a {end_h:02d}:{end_m:02d}")
        
        if self.week_days:
            parts.append(f"los {str(self.week_days)}")
        
        return ", ".join(parts)