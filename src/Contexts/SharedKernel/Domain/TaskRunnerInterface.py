from abc import ABC, abstractmethod
from collections.abc import Coroutine
from typing import Any, Callable


class TaskRunnerInterface(ABC):
    @abstractmethod
    def run(self, task: Callable[[], Coroutine[Any, Any, None]]) -> None:
        pass
