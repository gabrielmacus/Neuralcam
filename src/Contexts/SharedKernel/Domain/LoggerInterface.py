import abc


class LoggerInterface(abc.ABC):
    """
    https://stackoverflow.com/questions/6860186/log-info-vs-log-debug
    DEBUG: Information interesting for Developers, when trying to debug a problem.
    INFO: Information interesting for Support staff trying to figure out the context of a given
    error
    WARN to ERROR: Problems and Errors depending on the level of damage.
    """

    @abc.abstractmethod
    def info(self, message: str) -> None:
        pass

    @abc.abstractmethod
    def debug(self, message: str) -> None:
        pass

    @abc.abstractmethod
    def warn(self, message: str) -> None:
        pass

    @abc.abstractmethod
    def error(self, message: str) -> None:
        pass
