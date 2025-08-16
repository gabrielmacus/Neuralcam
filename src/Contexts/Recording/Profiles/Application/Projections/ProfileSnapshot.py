from src.Contexts.Recording.Profiles.Domain.Entities.Profile import Profile
from dataclasses import dataclass


@dataclass(frozen=True)
class ProfileSnapshot:
    id: str
    name: str
