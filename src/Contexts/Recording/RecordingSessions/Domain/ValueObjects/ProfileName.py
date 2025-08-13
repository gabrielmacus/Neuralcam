from src.Contexts.SharedKernel.Domain.ValueObjects.RequiredStringValueObject import (
    RequiredStringValueObject,
)


class ProfileName(RequiredStringValueObject):
    def __ensure_between_5_and_100_characters(self) -> None:
        if len(self.value) < 5 or len(self.value) > 100:
            raise ValueError("El nombre de perfil debe tener entre 5 y 100 caracteres.")

    def __post_init__(self):
        self.__ensure_between_5_and_100_characters()
