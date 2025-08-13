from dataclasses import dataclass
from urllib.parse import urlparse
from src.Contexts.SharedKernel.Domain.ValueObjects.StringValueObject import StringValueObject
from src.Contexts.Recording.RecordingSessions.Domain.Exceptions.InvalidRtspUriException import (
    InvalidRtspUriException,
)
from src.Contexts.Recording.RecordingSessions.Domain.Exceptions.MalformedUriException import (
    MalformedUriException,
)


@dataclass(frozen=True)
class Uri(StringValueObject):
    def __ensure_valid_rtsp_uri(self) -> None:
        if not self.value.startswith("rtsp://"):
            raise InvalidRtspUriException(self.value)

    def __ensure_well_formed_uri(self) -> None:
        try:
            parsed = urlparse(self.value)
            if not parsed.scheme or not parsed.netloc:
                raise MalformedUriException(self.value)
        except Exception:
            raise MalformedUriException(self.value)

    def __post_init__(self):
        self.__ensure_valid_rtsp_uri()
        self.__ensure_well_formed_uri()
