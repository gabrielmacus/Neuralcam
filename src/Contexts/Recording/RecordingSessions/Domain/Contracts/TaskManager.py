from abc import ABC, abstractmethod
from typing import Callable


class TaskManager(ABC):
    @abstractmethod
    def fire_and_forget(self, callback: Callable[[], None]) -> None:
        pass
