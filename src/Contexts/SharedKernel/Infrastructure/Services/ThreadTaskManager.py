from __future__ import annotations

import threading
from typing import Callable

from src.Contexts.SharedKernel.Domain.LoggerInterface import LoggerInterface
from src.Contexts.Recording.RecordingSessions.Domain.Contracts.TaskManager import TaskManager


class ThreadTaskManager(TaskManager):
    """
    Implementación del TaskManager usando threads para ejecutar tareas en segundo plano.
    """

    def __init__(self, logger: LoggerInterface):
        self.logger = logger

    def fire_and_forget(self, callback: Callable[[], None], daemon: bool = False) -> None:
        """
        Ejecuta una tarea en un thread separado sin esperar el resultado.

        Args:
            callback: Función a ejecutar en background
        """
        thread = threading.Thread(target=self._safe_execute, args=(callback,), daemon=daemon)
        thread.start()

    def _safe_execute(self, callback: Callable[[], None]) -> None:
        """
        Ejecuta el callback de forma segura, capturando cualquier excepción.

        Args:
            callback: Función a ejecutar
        """
        try:
            callback()
        except Exception as e:
            # En una implementación real, aquí se debería loggear el error
            # Por ahora solo imprimimos en stderr
            self.logger.error(f"Error ejecutando tarea en background: {e}")
