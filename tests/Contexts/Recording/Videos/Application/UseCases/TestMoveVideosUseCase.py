import pytest
from unittest.mock import Mock, call, ANY

from src.Contexts.Recording.Videos.Application.UseCases.MoveVideosUseCase import MoveVideosUseCase
from src.Contexts.Recording.Videos.Domain.Events.VideoUploadedDomainEvent import (
    VideoUploadedDomainEvent,
)
from src.Contexts.Recording.Videos.Domain.Events.VideoDeletedDomainEvent import (
    VideoDeletedDomainEvent,
)
from src.Contexts.Recording.Videos.Domain.Services.VideoMover import VideoMover
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
def move_videos_use_case(
    video_repository_mock, video_mover, logger_mock, uuid_generator_mock, event_bus_mock
):
    """Caso de uso real con dependencias mockeadas"""
    return MoveVideosUseCase(
        video_repository=video_repository_mock,
        video_mover=video_mover,
        logger=logger_mock,
        uuid_generator=uuid_generator_mock,
        event_bus=event_bus_mock,
    )


# Helper functions para refactorizar código común
def given_repository_find_videos_returns(repository_mock, directory_path, videos):
    """Configura el mock del repository para devolver videos específicos"""
    repository_mock.find_videos_in_directory.return_value = videos


def given_video_uploader_upload_returns(video_uploader_mock, upload_results):
    """Configura el mock del video uploader para devolver resultados de upload específicos"""
    video_uploader_mock.upload_overwrite.side_effect = upload_results


def given_videos_in_directory(directory_path, count=2):
    """Crea una lista de videos de prueba en un directorio específico"""
    videos = []
    for i in range(1, count + 1):
        video = VideoMother.create(
            path=f"{directory_path}/video{i}.mp4",
            name=f"video{i}",
            extension=".mp4",
        )
        videos.append(video)
    return videos


def given_video_exists(video_file_manager_mock, results: list[bool]):
    video_file_manager_mock.exists.side_effect = results


def moved_file_and_events_published_calls(
    video,
    destination_path,
):
    """Verifica orden exacto: exists → upload → delete → eventos para cada video usando mock manager"""
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
                    upload_destination=destination_path + video.name.value + video.extension.value,
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
def then_repository_find_videos_should_have_been_called_with(repository_mock, directory_path):
    """Verifica que se haya llamado al repositorio con el directorio correcto"""
    repository_mock.find_videos_in_directory.assert_called_once_with(directory_path)


def then_no_uploads_should_have_been_attempted(video_uploader_mock):
    """Verifica que no se hayan intentado uploads"""
    video_uploader_mock.upload_overwrite.assert_not_called()


def then_no_events_should_have_been_published(event_bus_mock):
    """Verifica que no se hayan publicado eventos"""
    event_bus_mock.publish.assert_not_called()


def then_operations_should_have_been_executed_in_order(mock_manager, expected_calls):
    """Verifica que las operaciones se hayan ejecutado en el orden correcto"""
    mock_manager.assert_has_calls(expected_calls)


def then_upload_should_have_been_called_times(video_uploader_mock, expected_count):
    """Verifica que el upload se haya llamado el número esperado de veces"""
    assert video_uploader_mock.upload_overwrite.call_count == expected_count


def then_video_exists_should_have_been_called_times(video_file_manager_mock, expected_count):
    """Verifica que la verificación de existencia se haya llamado el número esperado de veces"""
    assert video_file_manager_mock.exists.call_count == expected_count


def then_upload_should_have_been_called_with_video(video_uploader_mock, video, destination_path):
    """Verifica que el upload se haya llamado con el video y destino específicos"""
    video_uploader_mock.upload_overwrite.assert_called_with(video, destination_path)


def then_processed_and_failed_counts_should_be(result, expected_processed, expected_failed):
    """Verifica los contadores de procesados y fallidos"""
    processed_count, failed_count = result
    assert processed_count == expected_processed
    assert failed_count == expected_failed


def test_should_move_all_videos_successfully(
    move_videos_use_case, video_repository_mock, mock_manager, video_uploader_mock
):
    # Given
    directory_path = "/source/videos"
    destination_path = "s3://bucket/uploads/"
    videos = given_videos_in_directory(directory_path, count=2)

    given_repository_find_videos_returns(video_repository_mock, directory_path, videos)
    given_video_uploader_upload_returns(
        video_uploader_mock,
        ["s3://bucket/uploads/video1.mp4", "s3://bucket/uploads/video2.mp4"],
    )

    # When
    move_videos_use_case.execute(directory_path, destination_path)

    # Then
    then_repository_find_videos_should_have_been_called_with(video_repository_mock, directory_path)
    expected_calls = moved_file_and_events_published_calls(videos[0], destination_path)
    expected_calls.extend(moved_file_and_events_published_calls(videos[1], destination_path))
    then_operations_should_have_been_executed_in_order(mock_manager, expected_calls)


def test_should_handle_empty_directory_gracefully(
    move_videos_use_case, video_repository_mock, video_uploader_mock, event_bus_mock
):
    # Given
    directory_path = "/empty/directory"
    destination_path = "s3://bucket/uploads/"
    given_repository_find_videos_returns(video_repository_mock, directory_path, [])

    # When
    move_videos_use_case.execute(directory_path, destination_path)

    # Then
    then_repository_find_videos_should_have_been_called_with(video_repository_mock, directory_path)
    then_no_uploads_should_have_been_attempted(video_uploader_mock)
    then_no_events_should_have_been_published(event_bus_mock)


def test_should_continue_processing_when_individual_video_upload_fails(
    move_videos_use_case, video_repository_mock, mock_manager, video_uploader_mock
):
    # Given
    directory_path = "/source/videos"
    destination_path = "s3://bucket/uploads/"
    videos = given_videos_in_directory(directory_path, count=3)

    given_repository_find_videos_returns(video_repository_mock, directory_path, videos)
    given_video_uploader_upload_returns(
        video_uploader_mock,
        [
            "s3://bucket/uploads/video1.mp4",  # video1 success
            Exception("Upload failed for video2"),  # video2 fails
            "s3://bucket/uploads/video3.mp4",  # video3 success
        ],
    )

    # When
    move_videos_use_case.execute(directory_path, destination_path)

    # Then
    expected_calls = moved_file_and_events_published_calls(videos[0], destination_path)
    expected_calls.append(call.video_file_manager.exists(videos[1]))
    expected_calls.append(call.video_uploader.upload_overwrite(videos[1], destination_path))
    expected_calls.extend(moved_file_and_events_published_calls(videos[2], destination_path))
    then_operations_should_have_been_executed_in_order(mock_manager, expected_calls)


def test_should_end_gracefully_when_all_videos_fail(
    move_videos_use_case,
    video_repository_mock,
    mock_manager,
    video_uploader_mock,
    event_bus_mock,
    logger_mock,
):
    # Given
    directory_path = "/source/videos"
    destination_path = "s3://bucket/uploads/"
    videos = given_videos_in_directory(directory_path, count=2)

    given_repository_find_videos_returns(video_repository_mock, directory_path, videos)

    video_uploader_mock.upload_overwrite.side_effect = [
        Exception("Upload failed for video1"),
        Exception("Upload failed for video2"),
    ]

    # When
    move_videos_use_case.execute(directory_path, destination_path)

    # Then
    then_repository_find_videos_should_have_been_called_with(video_repository_mock, directory_path)
    then_upload_should_have_been_called_times(video_uploader_mock, 2)
    then_no_events_should_have_been_published(event_bus_mock)


def test_should_handle_video_not_found_exception_when_file_does_not_exist(
    move_videos_use_case,
    video_repository_mock,
    video_file_manager_mock,
    video_uploader_mock,
    event_bus_mock,
):
    """Test que verifica que se maneje correctamente cuando un archivo de video no existe"""
    # Given
    directory_path = "/source/videos"
    destination_path = "s3://bucket/uploads/"
    videos = given_videos_in_directory(directory_path, count=2)
    given_repository_find_videos_returns(video_repository_mock, directory_path, videos)
    # El primer video existe, el segundo no
    given_video_exists(video_file_manager_mock, [True, False])
    given_video_uploader_upload_returns(video_uploader_mock, ["s3://bucket/uploads/video1.mp4"])

    # When
    result = move_videos_use_case.execute(directory_path, destination_path)

    # Then
    then_repository_find_videos_should_have_been_called_with(video_repository_mock, directory_path)
    then_processed_and_failed_counts_should_be(result, 1, 1)
    then_video_exists_should_have_been_called_times(video_file_manager_mock, 2)
    then_upload_should_have_been_called_times(video_uploader_mock, 1)
    then_upload_should_have_been_called_with_video(video_uploader_mock, videos[0], destination_path)
