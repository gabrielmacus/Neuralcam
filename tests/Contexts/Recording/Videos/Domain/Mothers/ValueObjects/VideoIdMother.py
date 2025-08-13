import uuid
from typing import Optional
from src.Contexts.Recording.Videos.Domain.ValueObjects.VideoId import VideoId


class VideoIdMother:
    @staticmethod
    def create(video_id: Optional[str] = None) -> VideoId:
        """Crea un VideoId con valor opcional o random"""
        if video_id is None:
            video_id = str(uuid.uuid4())
        return VideoId(video_id)
