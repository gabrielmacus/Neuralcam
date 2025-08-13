from typing import Optional


class VideoFileOperationException(Exception):
    """Excepción lanzada cuando falla una operación de archivo de video"""
    
    def __init__(self, message: str = "Error en operación de archivo de video", original_exception: Optional[Exception] = None):
        self.message = message
        self.original_exception = original_exception
        super().__init__(self.message) 