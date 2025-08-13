from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from src.Contexts.SharedKernel.Domain.MessageBus.Query import Query
from src.Contexts.SharedKernel.Domain.MessageBus.QueryResponse import QueryResponse

R = TypeVar("R", bound=QueryResponse)


class QueryBus(ABC, Generic[R]):
    @abstractmethod
    def ask(self, query: Query) -> R:
        pass
