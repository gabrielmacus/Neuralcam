from datetime import datetime
from src.Contexts.SharedKernel.Domain.AggregateRoot import AggregateRoot
from ..ValueObjects.VideoId import VideoId
from ..ValueObjects.VideoPath import VideoPath
from ..ValueObjects.VideoName import VideoName
from ..ValueObjects.VideoExtension import VideoExtension
from ..Events.VideoUploadedDomainEvent import VideoUploadedDomainEvent
from ..Events.VideoDeletedDomainEvent import VideoDeletedDomainEvent


class Video(AggregateRoot):
    """Aggregate Root para representar un video"""

    def __init__(
        self,
        video_id: str,
        path: str,
        name: str,
        extension: str,
    ):
        super().__init__()
        self._id = VideoId(video_id)
        self._path = VideoPath(path)
        self._name = VideoName(name)
        self._extension = VideoExtension(extension)
        self._created_at = datetime.now()

    @classmethod
    def create_from_file_path(cls, video_id: str, file_path: str) -> "Video":
        """Crea un Video desde una ruta de archivo completa"""
        video_path = VideoPath(file_path)
        name = video_path.name_without_extension
        extension = video_path.extension

        return cls(
            video_id=video_id,
            path=file_path,
            name=name,
            extension=extension,
        )

    def mark_as_uploaded(self, upload_destination: str) -> None:
        """Marca el video como subido y registra el evento de dominio"""
        event = VideoUploadedDomainEvent(
            video_id=self._id.value,
            video_name=self._name.value,
            upload_destination=upload_destination,
            occurred_on=datetime.now(),
        )
        self.record_domain_event(event)

    def mark_as_deleted(self) -> None:
        """Marca el video como eliminado y registra el evento de dominio"""
        delete_event = VideoDeletedDomainEvent(
            video_id=self._id.value,
            video_name=self._name.value,
            video_path=self._path.value,
            occurred_on=datetime.now(),
        )
        self.record_domain_event(delete_event)

    # Propiedades de solo lectura
    @property
    def id(self) -> VideoId:
        return self._id

    @property
    def path(self) -> VideoPath:
        return self._path

    @property
    def name(self) -> VideoName:
        return self._name

    @property
    def extension(self) -> VideoExtension:
        return self._extension

    @property
    def created_at(self) -> datetime:
        return self._created_at
