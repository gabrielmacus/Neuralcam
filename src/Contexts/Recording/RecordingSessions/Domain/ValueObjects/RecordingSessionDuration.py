from dataclasses import dataclass


@dataclass(frozen=True)
class RecordingSessionDuration:
    value: int  # duración en segundos

    def __post_init__(self):
        self.__ensure_is_positive(self.value)
        self.__ensure_is_reasonable_duration(self.value)

    def __ensure_is_positive(self, value: int):
        if value <= 0:
            raise ValueError("La duración debe ser mayor a 0 segundos")

    def __ensure_is_reasonable_duration(self, value: int):
        # Máximo 24 horas (86400 segundos)
        max_duration = 24 * 60 * 60
        if value > max_duration:
            raise ValueError("La duración no puede exceder 24 horas")

    def __str__(self):
        return str(self.value)

    @property
    def duration_in_minutes(self) -> float:
        return self.value / 60

    @property
    def duration_in_hours(self) -> float:
        return self.value / 3600
