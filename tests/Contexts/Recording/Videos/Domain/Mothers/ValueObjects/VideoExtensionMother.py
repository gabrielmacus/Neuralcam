from typing import Optional
from src.Contexts.Recording.Videos.Domain.ValueObjects.VideoExtension import VideoExtension


class VideoExtensionMother:
    @staticmethod
    def create(extension: Optional[str] = None) -> VideoExtension:
        """Crea un VideoExtension con valor opcional o random"""
        if extension is None:
            extension = ".mp4"
        return VideoExtension(extension)
