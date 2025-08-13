from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class DomainEvent(ABC):

    @property
    @abstractmethod
    def event_name(self) -> str:
        pass
