import random
from datetime import datetime, timedelta
from typing import Optional

from src.Contexts.Recording.RecordingSessions.Domain.ValueObjects.StartDate import StartDate


class StartDateMother:

    @staticmethod
    def create(value: Optional[datetime] = None) -> StartDate:
        if value is None:
            # Generar fecha futura aleatoria entre ahora y 30 días en el futuro
            now = datetime.now()
            days_ahead = random.randint(1, 30)
            hours_ahead = random.randint(0, 23)
            minutes_ahead = random.randint(0, 59)
            value = now + timedelta(days=days_ahead, hours=hours_ahead, minutes=minutes_ahead)
        return StartDate(value)
