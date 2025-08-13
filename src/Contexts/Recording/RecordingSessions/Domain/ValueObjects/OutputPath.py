from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class OutputPath:
    value: str

    def __post_init__(self):
        self.__ensure_has_valid_extension(self.value)

    def __ensure_has_valid_extension(self, path: str) -> None:
        allowed_extensions = {".mkv"}
        file_extension = Path(path).suffix.lower()

        if file_extension not in allowed_extensions:
            raise ValueError(
                f"Extensión de archivo no válida. Extensiones permitidas: {', '.join(allowed_extensions)}"
            )

    def __str__(self):
        return self.value
