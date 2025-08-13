from typing import Optional
from src.Contexts.Recording.Videos.Domain.ValueObjects.VideoPath import VideoPath


class VideoPathMother:
    @staticmethod
    def create(path: Optional[str] = None) -> VideoPath:
        """Crea un VideoPath con valor opcional o random"""
        if path is None:
            path = "/tmp/videos/test_video.mp4"
        return VideoPath(path)
