import datetime
from abc import ABC, abstractmethod


class TimeProviderInterface(ABC):
    @abstractmethod
    def now_utc(self) -> datetime.datetime:
        pass

    @abstractmethod
    def now_local(self) -> datetime.datetime:
        pass
