from src.Contexts.SharedKernel.Domain.LoggerInterface import LoggerInterface
from src.Contexts.SharedKernel.Domain.UuidGenerator import UuidGenerator
from ...Domain.Services.RecordingService import RecordingService
from ...Domain.Contracts.TaskManager import TaskManager
from ...Domain.Entities.RecordingSession import RecordingSession
from ...Domain.Entities.Profile import Profile
from src.Contexts.SharedKernel.Domain.MessageBus.QueryBus import QueryBus
from src.Contexts.Recording.RecordingSessions.Application.Queries.GetProfilesQuery import (
    GetProfilesQuery,
)


class RecordProfilesUseCase:
    def __init__(
        self,
        query_bus: QueryBus,
        recording_service: RecordingService,
        task_manager: TaskManager,
        logger: LoggerInterface,
        uuid_generator: UuidGenerator,
    ):
        self._recording_service = recording_service
        self._task_manager = task_manager
        self._logger = logger
        self._uuid_generator = uuid_generator
        self._query_bus = query_bus

    def execute(self) -> None:
        """
        Obtiene todos los perfiles disponibles y los graba simultáneamente.
        Cada grabación se ejecuta en background usando TaskManager.
        """
        self._logger.debug("Iniciando grabación de perfiles")
        # Obtener perfiles disponibles
        profiles = self._query_bus.ask(GetProfilesQuery()).profiles
        self._logger.debug(f"Se encontraron {len(profiles)} perfiles para grabar")
        # Iniciar grabación de cada perfil simultáneamente
        for profile in profiles:
            try:
                self.__start_profile_recording(profile)

            except Exception as e:
                self._logger.error(
                    f"Error al iniciar grabación del perfil {profile.name.value}: {e}"
                )

    def __start_profile_recording(self, profile: Profile) -> None:
        """Inicia la grabación de un perfil específico"""
        self._logger.debug(f"Iniciando grabación del perfil: {profile.name.value}")
        self._recording_service.start_recording_session(
            uri=profile.uri,
            duration_seconds=profile.duration,
            profile_name=profile.name,
            profile_id=profile.id,
            profile_folder_path=profile.folder_path,
        )
