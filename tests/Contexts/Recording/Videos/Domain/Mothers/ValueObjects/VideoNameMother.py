from typing import Optional
from src.Contexts.Recording.Videos.Domain.ValueObjects.VideoName import VideoName


class VideoNameMother:
    @staticmethod
    def create(name: Optional[str] = None) -> VideoName:
        """Crea un VideoName con valor opcional o random"""
        if name is None:
            name = "test_video"
        return VideoName(name)
