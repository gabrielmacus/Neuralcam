class Profile:
    """Entidad que representa un perfil de grabación"""

    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name

    @classmethod
    def from_dict(cls, data: dict) -> "Profile":
        return cls(id=data["id"], name=data["name"])
