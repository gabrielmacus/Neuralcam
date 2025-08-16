from __future__ import annotations

from datetime import datetime
from src.Contexts.SharedKernel.Domain.LoggerInterface import LoggerInterface
from src.Contexts.SharedKernel.Domain.UuidGenerator import UuidGenerator
from src.Contexts.SharedKernel.Domain.EventBusInterface import EventBusInterface
from ..Contracts.TaskManager import TaskManager
from ..Contracts.VideoRecorder import VideoRecorder
from ..ValueObjects.OutputPath import OutputPath
from ..Contracts.PathEnsurer import PathEnsurer
from ..ValueObjects.Uri import Uri
from ..ValueObjects.RecordingSessionDuration import RecordingSessionDuration
from ..ValueObjects.ProfileId import ProfileId
from ..ValueObjects.ProfileName import ProfileName
from ..ValueObjects.ProfileFolderPath import ProfileFolderPath
from ..Entities.RecordingSession import RecordingSession
from src.Contexts.Recording.RecordingSessions.Domain.ValueObjects.RecordingSessionId import (
    RecordingSessionId,
)
from ..Entities.Profile import Profile


class RecordingService:
    def __init__(
        self,
        task_manager: TaskManager,
        video_recorder: VideoRecorder,
        path_ensurer: PathEnsurer,
        logger: LoggerInterface,
        uuid_generator: UuidGenerator,
        event_bus: EventBusInterface,
    ):
        self._task_manager = task_manager
        self._video_recorder = video_recorder
        self._path_ensurer = path_ensurer
        self._logger = logger
        self._uuid_generator = uuid_generator
        self._event_bus = event_bus

    def __get_output_path(
        self, profile_name: ProfileName, profile_folder_path: ProfileFolderPath
    ) -> OutputPath:
        return OutputPath(
            f"{profile_folder_path.value}/{profile_name.value}__{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.mkv"
        )

    def start_recording_session(
        self,
        uri: Uri,
        duration_seconds: RecordingSessionDuration,
        profile_name: ProfileName,
        profile_id: ProfileId,
        profile_folder_path: ProfileFolderPath,
    ) -> RecordingSession:
        self._logger.debug(f"Starting recording session for profile {profile_name.value}")
        output_path = self.__get_output_path(profile_name, profile_folder_path)

        self._logger.debug(f"Ensuring path {output_path.value}")
        self._path_ensurer.ensure_path(output_path)

        profile = Profile(
            profile_id=profile_id.value,
            profile_name=profile_name.value,
            uri=uri.value,
            duration_seconds=duration_seconds.value,
            folder_path=profile_folder_path.value,
        )
        recording_session = RecordingSession.create(
            recording_session_id=self._uuid_generator.generate(),
            profile=profile,
            start_date=datetime.now(),
        )

        # Callback que se ejecuta cuando termina la grabación
        def on_recording_finished(output_file_path: str) -> None:
            self._logger.debug(f"Recording finished for session {recording_session.id.value}")
            recording_session.finish(output_file_path)
            self._event_bus.publish(recording_session.pull_domain_events())

        self._logger.debug(
            f"Recording profile {profile_name.value} for {duration_seconds.value} seconds"
        )
        self._task_manager.fire_and_forget(
            lambda: self._video_recorder.record(
                uri, output_path, duration_seconds, on_recording_finished
            )
        )

        self._logger.debug(
            f"Recording session created for profile {profile_name.value}. Estimated end time: {recording_session.get_end_datetime()}"
        )

        return recording_session
