class InvalidRtspUriException(Exception):
    def __init__(self, uri: str):
        super().__init__(f"La URI '{uri}' debe ser un URI RTSP válido.")
        self.uri = uri
