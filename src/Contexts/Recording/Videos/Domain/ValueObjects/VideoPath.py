import os
from pathlib import Path
from src.Contexts.SharedKernel.Domain.ValueObjects.RequiredStringValueObject import RequiredStringValueObject


class VideoPath(RequiredStringValueObject):
    """Ruta completa del archivo de video"""
    
    def __init__(self, value: str):
        super().__init__(value)
        self._ensure_path_is_valid()
    
    def _ensure_path_is_valid(self):
        """Valida que la ruta sea válida"""
        if not self.value:
            raise ValueError("La ruta del video no puede estar vacía")
        
        # Validar que la ruta sea absoluta
        if not os.path.isabs(self.value):
            raise ValueError("La ruta del video debe ser absoluta")
    
    @property
    def directory(self) -> str:
        """Retorna el directorio que contiene el video"""
        return str(Path(self.value).parent)
    
    @property
    def filename(self) -> str:
        """Retorna el nombre del archivo con extensión"""
        return Path(self.value).name
    
    @property
    def name_without_extension(self) -> str:
        """Retorna el nombre del archivo sin extensión"""
        return Path(self.value).stem
    
    @property
    def extension(self) -> str:
        """Retorna la extensión del archivo"""
        return Path(self.value).suffix
    
    def exists(self) -> bool:
        """Verifica si el archivo existe"""
        return Path(self.value).exists()
    
    def file_size(self) -> int:
        """Retorna el tamaño del archivo en bytes"""
        if not self.exists():
            return 0
        return Path(self.value).stat().st_size 