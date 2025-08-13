from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from src.Contexts.SharedKernel.Domain.MessageBus.Query import Query
from src.Contexts.SharedKernel.Domain.MessageBus.QueryResponse import QueryResponse

R = TypeVar("R", bound=QueryResponse)
Q = TypeVar("Q", bound=Query)


class QueryHandler(ABC, Generic[Q, R]):
    @abstractmethod
    def handle(self, query: Q) -> R:
        pass
