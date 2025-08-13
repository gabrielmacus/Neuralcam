from abc import ABC, abstractmethod


class UuidGenerator(ABC):
    @abstractmethod
    def generate(self) -> str:
        pass
