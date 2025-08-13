from src.Contexts.SharedKernel.Domain.ValueObjects.RequiredStringValueObject import RequiredStringValueObject


class VideoName(RequiredStringValueObject):
    """Nombre del archivo de video sin extensión"""
    
    def __init__(self, value: str):
        super().__init__(value)
        self._ensure_name_is_valid()
    
    def _ensure_name_is_valid(self):
        """Valida que el nombre sea válido"""
        if not self.value.strip():
            raise ValueError("El nombre del video no puede estar vacío")
        
        # Validar caracteres prohibidos en nombres de archivo
        invalid_chars = ['<', '>', ':', '"', '|', '?', '*', '\\', '/']
        for char in invalid_chars:
            if char in self.value:
                raise ValueError(f"El nombre del video no puede contener el carácter '{char}'")
        
        # Validar longitud
        if len(self.value) > 255:
            raise ValueError("El nombre del video no puede exceder 255 caracteres") 