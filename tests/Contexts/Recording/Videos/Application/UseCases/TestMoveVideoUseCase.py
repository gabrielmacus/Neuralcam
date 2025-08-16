import pytest
from unittest.mock import Mock, call, ANY

from src.Contexts.Recording.Videos.Application.UseCases.MoveVideoUseCase import MoveVideoUseCase
from src.Contexts.Recording.Videos.Domain.Events.VideoUploadedDomainEvent import (
    VideoUploadedDomainEvent,
)
from src.Contexts.Recording.Videos.Domain.Events.VideoDeletedDomainEvent import (
    VideoDeletedDomainEvent,
)
from src.Contexts.Recording.Videos.Domain.Services.VideoMover import VideoMover
from src.Contexts.Recording.Videos.Domain.Services.VideoEnsurer import VideoEnsurer
from src.Contexts.Recording.Videos.Domain.Exceptions.VideoNotFoundException import (
    VideoNotFoundException,
)
from tests.Contexts.Recording.Videos.Domain.Mothers.VideoMother import VideoMother


@pytest.fixture
def mock_manager():
    """Mock manager central para rastrear orden de todas las operaciones"""
    return Mock()


@pytest.fixture
def video_repository_mock():
    return Mock()


@pytest.fixture
def configuration_mock():
    """Mock de Configuration con valores por defecto"""
    mock = Mock()
    mock.get_string.return_value = "/storage/videos"
    return mock


@pytest.fixture
def video_file_manager_mock(mock_manager):
    """Mock del video file manager vinculado al manager central"""
    mock = Mock()
    mock_manager.attach_mock(mock, "video_file_manager")
    mock.exists.return_value = True  # Por defecto, los archivos existen
    return mock


@pytest.fixture
def video_uploader_mock(mock_manager):
    """Mock del video uploader vinculado al manager central"""
    mock = Mock()
    mock_manager.attach_mock(mock, "video_uploader")
    return mock


@pytest.fixture
def event_bus_mock(mock_manager):
    """Mock del event bus vinculado al manager central"""
    mock = Mock()
    mock_manager.attach_mock(mock, "event_bus")
    return mock


@pytest.fixture
def logger_mock():
    """Mock del logger - NO vinculado al manager para evitar ruido en verificaciones de orden"""
    return Mock()


@pytest.fixture
def uuid_generator_mock():
    return Mock()


@pytest.fixture
def video_mover(video_file_manager_mock, video_uploader_mock, logger_mock):
    """Servicio de dominio real con mocks de infraestructura"""
    return VideoMover(
        video_file_manager=video_file_manager_mock,
        video_uploader=video_uploader_mock,
        logger=logger_mock,
    )


@pytest.fixture
def video_ensurer(video_repository_mock):
    """Servicio de dominio real con repositorio mockeado"""
    return VideoEnsurer(video_repository=video_repository_mock)


@pytest.fixture
def move_video_use_case(
    video_repository_mock,
    video_mover,
    video_ensurer,
    logger_mock,
    uuid_generator_mock,
    event_bus_mock,
    configuration_mock,
):
    """Caso de uso real con dependencias mockeadas"""
    return MoveVideoUseCase(
        video_repository=video_repository_mock,
        video_mover=video_mover,
        video_ensurer=video_ensurer,
        logger=logger_mock,
        uuid_generator=uuid_generator_mock,
        event_bus=event_bus_mock,
        configuration=configuration_mock,
    )


# Helper functions para refactorizar código común
def given_repository_find_by_path_returns(repository_mock, video_path, video):
    """Configura el mock del repository para devolver un video específico"""
    repository_mock.find_by_path.return_value = video


def given_video_uploader_upload_returns(video_uploader_mock, upload_result):
    """Configura el mock del video uploader para devolver resultado de upload específico"""
    video_uploader_mock.upload_overwrite.return_value = upload_result


def given_configuration_returns(configuration_mock, key, value):
    """Configura el mock de Configuration para devolver un valor específico"""
    configuration_mock.get_string.return_value = value


def given_video_in_path(video_path):
    """Crea un video de prueba en una ruta específica"""
    import os

    filename = os.path.basename(video_path)
    name_without_extension = os.path.splitext(filename)[0]
    extension = os.path.splitext(filename)[1]

    return VideoMother.create(
        path=video_path,
        name=name_without_extension,
        extension=extension,
    )


def given_video_exists(video_file_manager_mock, exists=True):
    video_file_manager_mock.exists.return_value = exists


def moved_file_and_events_published_calls(video, destination_path):
    """Verifica orden exacto: exists → upload → delete → eventos para el video usando mock manager"""
    expected_calls = []
    expected_calls.append(call.video_file_manager.exists(video))
    expected_calls.append(call.video_uploader.upload_overwrite(video, destination_path))
    expected_calls.append(call.video_file_manager.delete(video))
    expected_calls.append(
        call.event_bus.publish(
            [
                VideoUploadedDomainEvent(
                    video_id=video.id.value,
                    video_name=video.name.value,
                    upload_destination=destination_path,
                    occurred_on=ANY,
                ),
                VideoDeletedDomainEvent(
                    video_id=video.id.value,
                    video_name=video.name.value,
                    video_path=video.path.value,
                    occurred_on=ANY,
                ),
            ]
        )
    )
    return expected_calls


# Then functions para verificaciones comunes
def then_repository_find_by_path_should_have_been_called_with(repository_mock, video_path):
    """Verifica que se haya llamado al repositorio con la ruta correcta"""
    repository_mock.find_by_path.assert_called_once_with(video_path)


def then_configuration_should_have_been_called_with(configuration_mock, key, default):
    """Verifica que se haya llamado a la configuración con la clave correcta"""
    configuration_mock.get_string.assert_called_once_with(key, default)


def then_no_uploads_should_have_been_attempted(video_uploader_mock):
    """Verifica que no se hayan intentado uploads"""
    video_uploader_mock.upload_overwrite.assert_not_called()


def then_no_events_should_have_been_published(event_bus_mock):
    """Verifica que no se hayan publicado eventos"""
    event_bus_mock.publish.assert_not_called()


def then_operations_should_have_been_executed_in_order(mock_manager, expected_calls):
    """Verifica que las operaciones se hayan ejecutado en el orden correcto"""
    mock_manager.assert_has_calls(expected_calls)


def then_upload_should_have_been_called_with_video(video_uploader_mock, video, destination_path):
    """Verifica que el upload se haya llamado con el video y destino específicos"""
    video_uploader_mock.upload_overwrite.assert_called_with(video, destination_path)


def test_should_move_video_successfully(
    move_video_use_case,
    video_repository_mock,
    mock_manager,
    video_uploader_mock,
    configuration_mock,
):
    # Given
    video_path = "/source/videos/video1.mp4"
    base_path = "/storage/videos"
    expected_destination = f"{base_path}/video1.mp4"
    video = given_video_in_path(video_path)

    given_repository_find_by_path_returns(video_repository_mock, video_path, video)
    given_configuration_returns(configuration_mock, "video_storage_base_path", base_path)
    given_video_uploader_upload_returns(video_uploader_mock, f"{base_path}/video1.mp4")

    # When
    move_video_use_case.execute(video_path)

    # Then
    then_repository_find_by_path_should_have_been_called_with(video_repository_mock, video_path)
    then_configuration_should_have_been_called_with(
        configuration_mock, "video_storage_base_path", "/storage/videos"
    )
    expected_calls = moved_file_and_events_published_calls(video, expected_destination)
    then_operations_should_have_been_executed_in_order(mock_manager, expected_calls)


def test_should_use_default_path_when_configuration_not_found(
    move_video_use_case,
    video_repository_mock,
    mock_manager,
    video_uploader_mock,
    configuration_mock,
):
    # Given
    video_path = "/source/videos/video1.mp4"
    default_path = "/storage/videos"
    expected_destination = f"{default_path}/video1.mp4"
    video = given_video_in_path(video_path)

    given_repository_find_by_path_returns(video_repository_mock, video_path, video)
    # Configuration devuelve el valor por defecto
    given_configuration_returns(configuration_mock, "video_storage_base_path", default_path)
    given_video_uploader_upload_returns(video_uploader_mock, f"{default_path}/video1.mp4")

    # When
    move_video_use_case.execute(video_path)

    # Then
    then_repository_find_by_path_should_have_been_called_with(video_repository_mock, video_path)
    then_configuration_should_have_been_called_with(
        configuration_mock, "video_storage_base_path", "/storage/videos"
    )
    expected_calls = moved_file_and_events_published_calls(video, expected_destination)
    then_operations_should_have_been_executed_in_order(mock_manager, expected_calls)


def test_should_use_custom_base_path_from_configuration(
    move_video_use_case,
    video_repository_mock,
    mock_manager,
    video_uploader_mock,
    configuration_mock,
):
    # Given
    video_path = "/source/videos/video1.mp4"
    custom_base_path = "/custom/storage/path"
    expected_destination = f"{custom_base_path}/video1.mp4"
    video = given_video_in_path(video_path)

    given_repository_find_by_path_returns(video_repository_mock, video_path, video)
    given_configuration_returns(configuration_mock, "video_storage_base_path", custom_base_path)
    given_video_uploader_upload_returns(video_uploader_mock, f"{custom_base_path}/video1.mp4")

    # When
    move_video_use_case.execute(video_path)

    # Then
    then_repository_find_by_path_should_have_been_called_with(video_repository_mock, video_path)
    then_configuration_should_have_been_called_with(
        configuration_mock, "video_storage_base_path", "/storage/videos"
    )
    expected_calls = moved_file_and_events_published_calls(video, expected_destination)
    then_operations_should_have_been_executed_in_order(mock_manager, expected_calls)


def test_should_raise_error_when_video_not_found(
    move_video_use_case, video_repository_mock, video_uploader_mock, event_bus_mock
):
    # Given
    video_path = "/nonexistent/video.mp4"
    given_repository_find_by_path_returns(video_repository_mock, video_path, None)

    # When/Then
    with pytest.raises(VideoNotFoundException, match="Video no encontrado en la ruta"):
        move_video_use_case.execute(video_path)

    then_repository_find_by_path_should_have_been_called_with(video_repository_mock, video_path)
    then_no_uploads_should_have_been_attempted(video_uploader_mock)
    then_no_events_should_have_been_published(event_bus_mock)


def test_should_handle_upload_failure(
    move_video_use_case,
    video_repository_mock,
    video_uploader_mock,
    event_bus_mock,
    configuration_mock,
):
    # Given
    video_path = "/source/videos/video1.mp4"
    video = given_video_in_path(video_path)

    given_repository_find_by_path_returns(video_repository_mock, video_path, video)
    given_configuration_returns(configuration_mock, "video_storage_base_path", "/storage/videos")
    video_uploader_mock.upload_overwrite.side_effect = Exception("Upload failed")

    # When/Then
    with pytest.raises(Exception, match="Upload failed"):
        move_video_use_case.execute(video_path)

    then_repository_find_by_path_should_have_been_called_with(video_repository_mock, video_path)
    then_no_events_should_have_been_published(event_bus_mock)


def test_should_handle_video_file_not_exists(
    move_video_use_case,
    video_repository_mock,
    video_file_manager_mock,
    video_uploader_mock,
    event_bus_mock,
    configuration_mock,
):
    """Test que verifica que se maneje correctamente cuando el archivo de video no existe físicamente"""
    # Given
    video_path = "/source/videos/video1.mp4"
    video = given_video_in_path(video_path)

    given_repository_find_by_path_returns(video_repository_mock, video_path, video)
    given_configuration_returns(configuration_mock, "video_storage_base_path", "/storage/videos")
    given_video_exists(video_file_manager_mock, False)  # El archivo no existe físicamente

    # When/Then
    with pytest.raises(VideoNotFoundException):  # El VideoMover debería lanzar una excepción
        move_video_use_case.execute(video_path)

    then_repository_find_by_path_should_have_been_called_with(video_repository_mock, video_path)
    then_no_events_should_have_been_published(event_bus_mock)
