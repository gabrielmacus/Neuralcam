from dataclasses import dataclass, asdict
from datetime import datetime

from ..ValueObjects.ProfileId import ProfileId
from ..ValueObjects.ProfileName import ProfileName
from ..ValueObjects.Uri import Uri
from ..ValueObjects.RecordingSessionDuration import RecordingSessionDuration
from ..ValueObjects.ProfileFolderPath import ProfileFolderPath


@dataclass
class Profile:
    def __init__(
        self,
        profile_id: str,
        profile_name: str,
        uri: str,
        duration_seconds: int,
        folder_path: str,
    ):
        self._id = ProfileId(profile_id)
        self._name = ProfileName(profile_name)
        self._uri = Uri(uri)
        self._duration = RecordingSessionDuration(duration_seconds)
        self._folder_path = ProfileFolderPath(folder_path)
        self._created_at = datetime.now()

    @classmethod
    def from_dict(cls, profile_data: dict) -> "Profile":
        """Crea un Profile desde un diccionario de datos"""
        return cls(
            profile_id=profile_data["profile_id"],
            profile_name=profile_data["profile_name"],
            uri=profile_data["uri"],
            duration_seconds=profile_data["duration_seconds"],
            folder_path=profile_data["folder_path"],
        )

    def to_dict(self) -> dict:
        """Convierte el perfil a diccionario para serialización"""
        return asdict(self)

    # Propiedades de solo lectura
    @property
    def id(self) -> ProfileId:
        return self._id

    @property
    def name(self) -> ProfileName:
        return self._name

    @property
    def uri(self) -> Uri:
        return self._uri

    @property
    def duration(self) -> RecordingSessionDuration:
        return self._duration

    @property
    def folder_path(self) -> ProfileFolderPath:
        return self._folder_path
