import abc
from typing import Any, Optional


class Configuration(abc.ABC):
    """
    Interfaz para manejar la configuración y variables de entorno.
    Permite acceder a configuraciones de manera desacoplada desde el dominio.
    """

    @abc.abstractmethod
    def get(self, key: str, default: Optional[Any] = None) -> Any:
        """
        Obtiene un valor de configuración por su clave.

        Args:
            key: La clave de configuración a buscar
            default: Valor por defecto si la clave no existe

        Returns:
            El valor de configuración o el valor por defecto
        """
        pass

    @abc.abstractmethod
    def get_string(self, key: str, default: Optional[str] = None) -> str:
        """
        Obtiene un valor de configuración como string.

        Args:
            key: La clave de configuración a buscar
            default: Valor por defecto si la clave no existe

        Returns:
            El valor de configuración como string
        """
        pass

    @abc.abstractmethod
    def get_int(self, key: str, default: Optional[int] = None) -> int:
        """
        Obtiene un valor de configuración como entero.

        Args:
            key: La clave de configuración a buscar
            default: Valor por defecto si la clave no existe

        Returns:
            El valor de configuración como entero
        """
        pass

    @abc.abstractmethod
    def get_bool(self, key: str, default: Optional[bool] = None) -> bool:
        """
        Obtiene un valor de configuración como booleano.

        Args:
            key: La clave de configuración a buscar
            default: Valor por defecto si la clave no existe

        Returns:
            El valor de configuración como booleano
        """
        pass

    @abc.abstractmethod
    def get_float(self, key: str, default: Optional[float] = None) -> float:
        """
        Obtiene un valor de configuración como float.

        Args:
            key: La clave de configuración a buscar
            default: Valor por defecto si la clave no existe

        Returns:
            El valor de configuración como float
        """
        pass
