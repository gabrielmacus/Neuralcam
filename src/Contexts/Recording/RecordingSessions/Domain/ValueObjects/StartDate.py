from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class StartDate:
    value: datetime

    def __post_init__(self):
        self.__ensure_is_valid_datetime(self.value)
        self.__ensure_is_not_in_past(self.value)

    def __ensure_is_valid_datetime(self, value: datetime):
        if not isinstance(value, datetime):
            raise ValueError("El valor debe ser un objeto datetime válido")

        # Validar que no sea una fecha muy antigua (más de 100 años)
        min_date = datetime(1924, 1, 1)
        if value < min_date:
            raise ValueError("La fecha de inicio no puede ser anterior a 1924")

        # Validar que no sea una fecha muy futura (más de 10 años)
        max_date = datetime.now().replace(year=datetime.now().year + 10)
        if value > max_date:
            raise ValueError("La fecha de inicio no puede ser más de 10 años en el futuro")

    def __ensure_is_not_in_past(self, value: datetime):
        if value < datetime.now():
            raise ValueError("La fecha de inicio no puede estar en el pasado")

    def __str__(self):
        return self.value.isoformat()

    @property
    def year(self) -> int:
        return self.value.year

    @property
    def month(self) -> int:
        return self.value.month

    @property
    def day(self) -> int:
        return self.value.day

    @property
    def hour(self) -> int:
        return self.value.hour

    @property
    def minute(self) -> int:
        return self.value.minute

    def is_before(self, other: "StartDate") -> bool:
        return self.value < other.value

    def is_after(self, other: "StartDate") -> bool:
        return self.value > other.value
