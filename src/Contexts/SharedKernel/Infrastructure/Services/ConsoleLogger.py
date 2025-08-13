from __future__ import annotations

import sys
from datetime import datetime

from src.Contexts.SharedKernel.Domain.LoggerInterface import LoggerInterface


class ConsoleLogger(LoggerInterface):
    """
    Implementación del LoggerInterface que imprime mensajes en la consola.
    """

    def debug(self, message: str) -> None:
        """Registra un mensaje de debug en stdout."""
        self._log("DEBUG", message, sys.stdout)

    def info(self, message: str) -> None:
        """Registra un mensaje informativo en stdout."""
        self._log("INFO", message, sys.stdout)

    def warn(self, message: str) -> None:
        """Registra un mensaje de advertencia en stderr."""
        self._log("WARNING", message, sys.stderr)

    def error(self, message: str) -> None:
        """Registra un mensaje de error en stderr."""
        self._log("ERROR", message, sys.stderr)

    def _log(self, level: str, message: str, output_stream) -> None:
        """
        Método interno para formatear y escribir el mensaje de log.

        Args:
            level: Nivel del log (DEBUG, INFO, WARNING, ERROR)
            message: Mensaje a loggear
            output_stream: Stream donde escribir (stdout o stderr)
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted_message = f"[{timestamp}] [{level}] {message}"
        print(formatted_message, file=output_stream)
        output_stream.flush()
