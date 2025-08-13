from __future__ import annotations

from abc import ABC, abstractmethod

from src.Contexts.SharedKernel.Domain.DomainEvent import DomainEvent


class EventBusInterface(ABC):
    @abstractmethod
    def publish(self, events: list[DomainEvent]) -> None:
        pass
