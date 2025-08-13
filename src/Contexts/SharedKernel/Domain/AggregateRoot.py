from dataclasses import dataclass
from typing import List

from src.Contexts.SharedKernel.Domain.DomainEvent import DomainEvent


@dataclass
class AggregateRoot:

    def __init__(self):
        self.domain_events: List[DomainEvent] = []

    def pull_domain_events(self) -> List[DomainEvent]:
        events = self.domain_events.copy()
        self.domain_events.clear()
        return events

    def record_domain_event(self, domain_event: DomainEvent) -> None:
        self.domain_events.append(domain_event)
