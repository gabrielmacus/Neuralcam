from dataclasses import dataclass


@dataclass(frozen=True)
class ProfileDTO:
    profile_id: str
    profile_name: str
    uri: str
    duration_seconds: int
    folder_path: str
