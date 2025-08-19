from datetime import datetime
from typing import Optional

from src.Contexts.Recording.Profiles.Domain.ValueObjects.ScheduleConfigurationValueObject import ScheduleConfigurationValueObject


class Profile:
    """Entidad que representa un perfil de grabación"""

    def __init__(
        self, 
        id: str, 
        name: str, 
        schedule_configuration: Optional[ScheduleConfigurationValueObject] = None
    ):
        self.id = id
        self.name = name
        self.schedule_configuration = schedule_configuration

    def is_active_at(self, check_datetime: datetime) -> bool:
        """
        Determina si el perfil está activo en una fecha/hora dada.
        Si no hay configuración de horario, el perfil está siempre activo.
        """
        if self.schedule_configuration is None:
            return True
        
        return self.schedule_configuration.is_active_at(check_datetime)

    def is_active_now(self) -> bool:
        """Determina si el perfil está activo en este momento"""
        return self.is_active_at(datetime.now())

    def set_schedule_configuration(self, schedule_configuration: ScheduleConfigurationValueObject):
        """Establece o actualiza la configuración de horario del perfil"""
        self.schedule_configuration = schedule_configuration

    def clear_schedule_configuration(self):
        """Elimina la configuración de horario, haciendo que el perfil esté siempre activo"""
        self.schedule_configuration = None

    def has_schedule_configuration(self) -> bool:
        """Verifica si el perfil tiene configuración de horario"""
        return self.schedule_configuration is not None

    @classmethod
    def from_dict(cls, data: dict) -> "Profile":
        """Crea un Profile desde un diccionario"""
        schedule_config = None
        if data.get("schedule_configuration"):
            schedule_config = ScheduleConfigurationValueObject.from_dict(data["schedule_configuration"])
        
        return cls(
            id=data["id"], 
            name=data["name"],
            schedule_configuration=schedule_config
        )

    def to_dict(self) -> dict:
        """Convierte el perfil a diccionario para serialización"""
        return {
            "id": self.id,
            "name": self.name,
            "schedule_configuration": self.schedule_configuration.to_dict() if self.schedule_configuration else None
        }
