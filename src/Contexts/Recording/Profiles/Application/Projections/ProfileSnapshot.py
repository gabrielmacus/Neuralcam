from src.Contexts.Recording.Profiles.Domain.Entities.Profile import Profile
from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass(frozen=True)
class ProfileSnapshot:
    """Snapshot que representa el estado proyectado de un perfil desde otro microservicio"""
    id: str
    name: str
    # Campos de configuración de horario que vienen del otro microservicio
    schedule_configuration: Optional[Dict[str, Any]] = None
