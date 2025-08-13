class MalformedUriException(Exception):
    def __init__(self, uri: str):
        super().__init__(f"La URI '{uri}' no está bien formada.")
        self.uri = uri
