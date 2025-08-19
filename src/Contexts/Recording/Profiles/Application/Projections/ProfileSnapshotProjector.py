from src.Contexts.Recording.Profiles.Application.Projections.ProfileSnapshot import ProfileSnapshot
from src.Contexts.Recording.Profiles.Domain.Entities.Profile import Profile
from src.Contexts.Recording.Profiles.Domain.ValueObjects.ScheduleConfigurationValueObject import ScheduleConfigurationValueObject
from dataclasses import asdict

# from src.Contexts.Recording.Profiles.Domain.Contracts.ProfileRepository import ProfileRepository


class ProfileSnapshotProjector:
    """Proyecta el estado actual de un perfil de grabación desde otro microservicio"""

    def __init__(self, repository):  # ProfileRepository cuando esté implementado
        self._repository = repository

    def project(self, snapshot: ProfileSnapshot):
        """
        Proyecta el estado actual de un perfil de grabación.
        Convierte la configuración de horario desde el snapshot al domain model.
        """
        snapshot_dict = asdict(snapshot)
        
        # Procesar configuración de horario si existe
        if snapshot_dict.get("schedule_configuration"):
            schedule_config_data = snapshot_dict["schedule_configuration"]
            
            # Validar y convertir la configuración de horario
            try:
                schedule_config = ScheduleConfigurationValueObject.from_dict(schedule_config_data)
                snapshot_dict["schedule_configuration"] = schedule_config.to_dict()
            except (ValueError, KeyError) as e:
                # Log error y continuar sin configuración de horario
                # TODO: Add proper logging
                print(f"Error procesando configuración de horario para perfil {snapshot.id}: {e}")
                snapshot_dict["schedule_configuration"] = None
        
        # Crear y guardar la entidad Profile
        profile = Profile.from_dict(snapshot_dict)
        self._repository.save(profile)

    def project_from_dict(self, profile_data: dict):
        """
        Proyecta un perfil directamente desde un diccionario.
        Útil cuando se reciben datos desde mensajes de otro microservicio.
        """
        # Crear snapshot desde el diccionario
        snapshot = ProfileSnapshot(
            id=profile_data["id"],
            name=profile_data["name"],
            schedule_configuration=profile_data.get("schedule_configuration")
        )
        
        # Proyectar usando el método principal
        self.project(snapshot)
