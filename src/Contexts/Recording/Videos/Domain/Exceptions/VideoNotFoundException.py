class VideoNotFoundException(Exception):
    """Excepción lanzada cuando no se encuentra un video"""
    
    def __init__(self, message: str = "Video no encontrado"):
        self.message = message
        super().__init__(self.message) 