class ConfigurationException(Exception):
    """Excepción base para errores de configuración."""

    pass


class ConfigurationKeyNotFoundException(ConfigurationException):
    """Excepción lanzada cuando no se encuentra una clave de configuración."""

    def __init__(self, key: str):
        super().__init__(f"Configuration key '{key}' not found and no default provided")
        self.key = key


class ConfigurationConversionException(ConfigurationException):
    """Excepción lanzada cuando no se puede convertir un valor de configuración."""

    def __init__(self, key: str, value, target_type: str):
        super().__init__(f"Cannot convert configuration key '{key}' to {target_type}: {value}")
        self.key = key
        self.value = value
        self.target_type = target_type
