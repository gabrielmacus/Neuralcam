import pytest
from unittest.mock import Mock

from src.Contexts.Recording.Videos.Domain.Services.VideoEnsurer import VideoEnsurer
from src.Contexts.Recording.Videos.Domain.Exceptions.VideoNotFoundException import (
    VideoNotFoundException,
)
from tests.Contexts.Recording.Videos.Domain.Mothers.VideoMother import VideoMother


@pytest.fixture
def video_repository_mock():
    return Mock()


@pytest.fixture
def video_ensurer(video_repository_mock):
    return VideoEnsurer(video_repository=video_repository_mock)


def test_should_return_video_when_exists(video_ensurer, video_repository_mock):
    # Given
    video_path = "/source/videos/test.mp4"
    expected_video = VideoMother.create(path=video_path, name="test", extension=".mp4")
    video_repository_mock.find_by_path.return_value = expected_video

    # When
    result = video_ensurer.ensure_video(video_path)

    # Then
    assert result == expected_video
    video_repository_mock.find_by_path.assert_called_once_with(video_path)


def test_should_raise_exception_when_video_not_found(video_ensurer, video_repository_mock):
    # Given
    video_path = "/nonexistent/video.mp4"
    video_repository_mock.find_by_path.return_value = None

    # When/Then
    with pytest.raises(
        VideoNotFoundException, match="Video no encontrado en la ruta: /nonexistent/video.mp4"
    ):
        video_ensurer.ensure_video(video_path)

    video_repository_mock.find_by_path.assert_called_once_with(video_path)


def test_should_propagate_repository_exceptions(video_ensurer, video_repository_mock):
    # Given
    video_path = "/source/videos/test.mp4"
    repository_error = Exception("Repository connection error")
    video_repository_mock.find_by_path.side_effect = repository_error

    # When/Then
    with pytest.raises(Exception, match="Repository connection error"):
        video_ensurer.ensure_video(video_path)

    video_repository_mock.find_by_path.assert_called_once_with(video_path)
