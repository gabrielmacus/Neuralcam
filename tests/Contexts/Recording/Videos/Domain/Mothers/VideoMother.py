from typing import Optional
from src.Contexts.Recording.Videos.Domain.Entities.Video import Video
from .ValueObjects.VideoIdMother import VideoIdMother
from .ValueObjects.VideoPathMother import VideoPathMother
from .ValueObjects.VideoNameMother import VideoNameMother
from .ValueObjects.VideoExtensionMother import VideoExtensionMother


class VideoMother:
    @staticmethod
    def create(
        video_id: Optional[str] = None,
        path: Optional[str] = None,
        name: Optional[str] = None,
        extension: Optional[str] = None,
    ) -> Video:
        """Crea un Video con parámetros opcionales usando object mothers"""
        return Video(
            video_id=video_id or VideoIdMother.create().value,
            path=path or VideoPathMother.create().value,
            name=name or VideoNameMother.create().value,
            extension=extension or VideoExtensionMother.create().value,
        )
