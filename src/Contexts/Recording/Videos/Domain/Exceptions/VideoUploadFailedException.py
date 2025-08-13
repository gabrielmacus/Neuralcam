from typing import Optional


class VideoUploadFailedException(Exception):
    """Excepción lanzada cuando falla la subida de un video"""
    
    def __init__(self, message: str = "Error al subir el video", original_exception: Optional[Exception] = None):
        self.message = message
        self.original_exception = original_exception
        super().__init__(self.message) 