from src.Contexts.Recording.Profiles.Application.Projections.ProfileSnapshot import ProfileSnapshot
from src.Contexts.Recording.Profiles.Domain.Entities.Profile import Profile
from dataclasses import asdict

# from src.Contexts.Recording.Profiles.Domain.Contracts.ProfileRepository import ProfileRepository


class ProfileSnapshotProjector:
    """Proyecta el estado actual de un perfil de grabación"""

    def __init__(self, repository):  # ProfileRepository cuando esté implementado
        self._repository = repository

    def project(self, snapshot: ProfileSnapshot):
        """Proyecta el estado actual de un perfil de grabación"""
        profile = Profile.from_dict(asdict(snapshot))
        self._repository.save(profile)
