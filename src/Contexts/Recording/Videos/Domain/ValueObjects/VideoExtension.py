from src.Contexts.SharedKernel.Domain.ValueObjects.RequiredStringValueObject import RequiredStringValueObject


class VideoExtension(RequiredStringValueObject):
    """Extensión del archivo de video"""
    
    # Extensiones de video soportadas
    SUPPORTED_EXTENSIONS = {'.mkv', '.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm', '.m4v'}
    
    def __init__(self, value: str):
        super().__init__(value)
        self._ensure_extension_is_valid()
    
    def _ensure_extension_is_valid(self):
        """Valida que la extensión sea válida"""
        if not self.value:
            raise ValueError("La extensión del video no puede estar vacía")
        
        # Asegurar que empiece con punto
        if not self.value.startswith('.'):
            self._value = f'.{self.value}'
        
        # Convertir a minúsculas para comparación
        extension_lower = self.value.lower()
        
        if extension_lower not in self.SUPPORTED_EXTENSIONS:
            supported = ', '.join(self.SUPPORTED_EXTENSIONS)
            raise ValueError(f"Extensión de video no soportada: {self.value}. Extensiones soportadas: {supported}")
    
    def is_video_extension(self) -> bool:
        """Verifica si es una extensión de video válida"""
        return self.value.lower() in self.SUPPORTED_EXTENSIONS 